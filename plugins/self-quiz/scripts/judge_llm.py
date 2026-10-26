#!/usr/bin/env python3
"""self-quiz LLM 判官（仅 judge: llm_free 类题使用）。

端点优先级：AI_Core gpt-6.1-sol（闭源 SOTA，主判）→ Zcode glm-5.3-flash（兜底）。
端点凭据从 QA_JUDGE_CONFIG 指向的 JSON 读取（由 harness 从本机 models.json 生成，
文件位于 gitignored 的 results/ 下，绝不入库）。

用法：
  judge_llm.py --question <题面.md> --expected <标准答案.md> --answer <作答.txt>
输出（stdout 首行）：
  PASS …      判官通过（附理由）
  FAIL …      判官否决（附理由与差异）
退出码 3 表示判官不可用（配置缺失/两个端点都失败）——此时不落任何记录。
"""
import argparse
import json
import os
import sys
import urllib.request
from pathlib import Path

SYSTEM_PROMPT = """你是严格的技术判官。给你：一道自检题、题库标准答案（含出处与判分要点）、学生的作答。
判分铁律：
1. 只信标准答案与出处，绝不采信作答的自洽性——流利地复述一套自创协议同样是错。
2. 逐字节要求的内容，空格/大小写/换行/数字格式（0 vs 0.00）都算差异。
3. 集合类答案漏项、错拼、多余项任一即不过。
4. 部分正确、含糊其辞（"通常是/大概"）、以通用惯例替代题目要求的具体契约，一律不过。
5. 不给同情分；判分要点之外不做善意推断。
输出格式（务必遵守）：
第一行：PASS 或 FAIL
随后：不超过 120 字的判语；FAIL 时精确指出与标准答案的差异，并给出出处要点。"""


def _extract(path: Path, strip_fm: bool = True) -> str:
    text = path.read_text(encoding="utf-8")
    if strip_fm and text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            text = parts[2]
    return text.strip()


def _chat(base_url: str, api_key: str, model: str, system: str,
          user: str, timeout_s: int) -> str:
    url = base_url.rstrip("/") + "/chat/completions"
    payload = json.dumps({
        "model": model,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        "max_tokens": 512,
        "temperature": 0,
    }).encode("utf-8")
    req = urllib.request.Request(
        url, data=payload, method="POST",
        headers={"Content-Type": "application/json",
                 "Authorization": f"Bearer {api_key}"})
    with urllib.request.urlopen(req, timeout=timeout_s) as resp:
        body = json.loads(resp.read().decode("utf-8"))
    return body["choices"][0]["message"]["content"] or ""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--question", required=True)
    ap.add_argument("--expected", required=True)
    ap.add_argument("--answer", required=True)
    args = ap.parse_args()

    cfg_path = os.environ.get("QA_JUDGE_CONFIG", "")
    cfg = {}
    if cfg_path and Path(cfg_path).is_file():
        try:
            cfg = json.loads(Path(cfg_path).read_text(encoding="utf-8"))
        except Exception as exc:  # noqa: BLE001
            print(f"ERROR: judge config 解析失败: {exc}", file=sys.stderr)
            return 3
    else:
        print("ERROR: QA_JUDGE_CONFIG 未设置或文件不存在（llm_free 题不可用）",
              file=sys.stderr)
        return 3

    user = (f"# 题面\n{_extract(Path(args.question))}\n\n"
            f"# 标准答案（判分唯一依据）\n{_extract(Path(args.expected))}\n\n"
            f"# 学生作答\n{_extract(Path(args.answer), strip_fm=False)}\n\n"
            "请判定并按格式输出。")

    attempts = []
    if cfg.get("primary"):
        attempts.append(("primary", cfg["primary"]))
    if cfg.get("fallback"):
        attempts.append(("fallback", cfg["fallback"]))
    for label, ep in attempts:
        try:
            reply = _chat(ep["base_url"], ep["api_key"], ep["model"],
                          SYSTEM_PROMPT, user,
                          int(cfg.get("timeout_s", 60)))
            first = reply.strip().splitlines()[0].strip() if reply.strip() else ""
            rest = " ".join(reply.strip().splitlines()[1:]).strip()
            if first.upper().startswith("PASS"):
                print("PASS" + (f"（{label}）{rest}" if rest else ""))
                return 0
            if first.upper().startswith("FAIL"):
                print("FAIL" + (f"（{label}）{rest}" if rest else ""))
                return 1
            # 判官没按格式回答：换下一个端点
            print(f"[warn] {label} 返回未按格式：{reply[:120]}", file=sys.stderr)
        except Exception as exc:  # noqa: BLE001
            print(f"[warn] {label} 调用失败: {type(exc).__name__}: {exc}",
                  file=sys.stderr)
    print("ERROR: 两个判官端点均不可用", file=sys.stderr)
    return 3


if __name__ == "__main__":
    sys.exit(main())

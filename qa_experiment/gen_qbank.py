#!/usr/bin/env python3
"""Generate per-task self-quiz question banks from ICAE oracle data.

Sources (STRICTLY agent-legitimately-obtainable material — never the hidden or
enhanced suites):
  - ICAE-EVAL/user_agent/prd_json/<alias>.json
      oracle_data.hidden_constraints  (oracle cards; obtainable by asking)
      oracle_data.golden_api_signature (obtainable via API-alignment questions)
      public_test_cases               (obtainable by asking for test cases)
  - comparison/run_records_5b3b6db7/run_settings.json
      per-suite expected/actual samples -> wrong_answer_pattern enrichment

Output: <out>/<alias>/{questions,answers}/QXXX.md  in the self-quiz bank format
(consumed by plugins/self-quiz/scripts/quiz.sh `start`/`grade`).

Question mix per task (≤8):
  T1 set_match  — union of dispatcher input field names
  T1 set_match  — full legal value set of the detected routing field (if any)
  T2 byte_equal — up to 4 "exact stdout for this public case" questions
  T4 keyword    — up to 2 conditional oracle cards (exact quoted literals)
  T6 keyword    — golden API signature method/arg tokens

Usage:
  python3 gen_qbank.py [--aliases realcode@003,realcode@024] [--out ../qa_banks]
Default aliases: the 5-repo pilot set.
"""
import argparse
import base64
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
PRD_DIR = REPO / "ICAE-EVAL" / "user_agent" / "prd_json"
RUN_SETTINGS = REPO / "comparison" / "run_records_5b3b6db7" / "run_settings.json"
DEFAULT_OUT = REPO / "qa_banks"
PILOT = ["realcode@003", "realcode@024", "realcode@020", "realcode@026", "realcode@002"]

# Primary deviation class per alias (from 理解偏差案例库 §4/§5/§6); default B.
DEVIATION = {
    "002": "C", "003": "B", "004": "C", "005": "B", "007": "C", "011": "C",
    "014": "C", "016": "B", "017": "E", "018": "C", "019": "B", "020": "B",
    "021": "A", "022": "A", "024": "A", "025": "A", "026": "A", "027": "A",
    "028": "A", "029": "B", "030": "C", "031": "E", "033": "A", "034": "B",
    "035": "A", "036": "A", "037": "A", "038": "A", "039": "A", "040": "C",
    "041": "B", "042": "C", "043": "A", "044": "B", "045": "A", "046": "E",
    "047": "C", "048": "B", "049": "D", "050": "E", "001": "A", "006": "A",
    "008": "A", "010": "A", "012": "A", "015": "A",
}


def fm_escape(text: str) -> str:
    return text.strip()


def detect_route_field(ptc: dict):
    """Find the dispatcher's routing field: a short string field present in
    every feature with (mostly) one value per feature and >=2 distinct values.
    Returns (field, all_values) or None."""
    common_keys = None
    per_feature_vals = []
    for fname, spec in ptc.items():
        keys, vals = set(), {}
        for c in spec.get("cases", []):
            inp = c.get("input")
            if isinstance(inp, dict):
                for k, v in inp.items():
                    if isinstance(v, str) and 0 < len(v) < 48:
                        keys.add(k)
                        vals.setdefault(k, set()).add(v)
        common_keys = keys if common_keys is None else (common_keys & keys)
        per_feature_vals.append(vals)
    if not common_keys:
        return None
    best = None
    for k in sorted(common_keys):
        all_vals, fvals, ok = set(), [], True
        for vals in per_feature_vals:
            vs = vals.get(k, set())
            if not vs:
                ok = False
                break
            fvals.append(sorted(vs)[0])
            all_vals |= vs
        if not ok or len(set(fvals)) < 2:
            continue
        if best is None or len(all_vals) > len(best[1]):
            best = (k, all_vals)
    return best


def extract_keywords(resp: str, cap: int = 6):
    """Quoted literals + key=value tokens (+ backticked spans) from a card."""
    toks = []
    for pat in (r"'([^'\n]{2,60})'", r"\"([^\"\n]{2,60})\"", r"`([^`\n]{2,60})`",
                r"\b([a-z_][a-z0-9_]*=[A-Za-z0-9_.<>{}#\\n-]+)",
                r"\b(error=[a-z_]+|notice=[a-z_]+)"):
        for m in re.findall(pat, resp):
            t = m.strip()
            if t and t not in toks:
                toks.append(t)
    return toks[:cap]


def pick_conditional_cards(hc: list, n: int = 2):
    out = []
    for c in hc:
        cid = c.get("constraint_id") or c.get("id", "")
        if cid.startswith(("HARNESS", "ARCH", "TC_")):
            continue
        resp = c.get("oracle_response", "") or ""
        if not (60 <= len(resp) <= 700):
            continue
        if not re.search(r"\b(when|if|unless|while)\b", resp, re.I):
            continue
        toks = extract_keywords(resp)
        if len(toks) >= 2:
            out.append((len(toks), cid, resp, toks))
    out.sort(key=lambda x: -x[0])
    return out[:n]


def api_signature_tokens(sig: str, cap: int = 8):
    toks = re.findall(r"\b([A-Za-z_][A-Za-z0-9_]*)(?=\s*\()", sig)
    toks += re.findall(r"\b([a-z_][a-z0-9_]*)(?=:)", sig)
    seen, out = set(), []
    for t in toks:
        if t not in seen and len(t) > 2:
            seen.add(t)
            out.append(t)
    return out[:cap]


def wrong_patterns(run_repos: dict, alias: str):
    """First-line digests of the baseline run's actual outputs (wrong patterns)."""
    pats = []
    obj = (run_repos.get(alias) or {}).get("objective") or {}
    for suite in ("public_visible", "hidden", "enhanced"):
        sample = ((obj.get(suite) or {}).get("sample") or {})
        actual = (sample.get("actual") or "").strip()
        if sample.get("kind") == "mismatch" and actual:
            first = actual.splitlines()[0][:60]
            if first and first not in pats:
                pats.append(first)
    return pats


def write_question(qdir: Path, adir: Path, qid: str, meta: dict,
                   question: str, answer_body: str) -> str:
    (qdir / f"{qid}.md").write_text(
        "---\n"
        f"id: {qid}\n"
        f"title: {meta['title']}\n"
        f"type: {meta['type']}\n"
        f"deviation_type: {meta['dev']}\n"
        f"created: {meta['created']}\n"
        "---\n"
        f"{question.strip()}\n",
        encoding="utf-8")
    extra = (f"expected_b64: {meta['expected_b64']}\n"
             if "expected_b64" in meta else "")
    (adir / f"{qid}.md").write_text(
        "---\n"
        f"id: {qid}\n"
        f"judge: {meta['judge']}\n"
        + extra +
        "---\n"
        f"{answer_body.strip()}\n",
        encoding="utf-8")
    return qid


def gen_for_alias(alias: str, out_root: Path, run_repos: dict, stats: dict):
    prd_path = PRD_DIR / f"{alias}.json"
    if not prd_path.is_file():
        print(f"[{alias}] SKIP: no prd_json")
        return
    d = json.loads(prd_path.read_text(encoding="utf-8"))
    od = d.get("oracle_data", {})
    ptc = d.get("public_test_cases", {}) or {}
    if not ptc:
        print(f"[{alias}] SKIP: no public_test_cases")
        return
    dev = DEVIATION.get(alias.split("@")[-1], "B")
    from datetime import date
    created = date.today().isoformat()
    qdir = out_root / alias / "questions"
    adir = out_root / alias / "answers"
    qdir.mkdir(parents=True, exist_ok=True)
    adir.mkdir(parents=True, exist_ok=True)
    pats = wrong_patterns(run_repos, alias)
    n = 0
    ids = []

    def qid():
        nonlocal n
        n += 1
        return f"Q{n:03d}"

    # ── T1: input field union ────────────────────────────────────────────────
    fields = set()
    for spec in ptc.values():
        for c in spec.get("cases", []):
            inp = c.get("input")
            if isinstance(inp, dict):
                fields |= set(inp.keys())
    if fields:
        fl = sorted(fields)
        ids.append(write_question(qdir, adir, qid(),
            {"title": "dispatcher input field union", "type": "T1", "dev": "A",
             "created": created, "judge": "set_match"},
            "List the union of ALL top-level field names that appear in the "
            "dispatcher input JSON across every public test case. One item per "
            "line, exact spelling, no extras.",
            "# 标准答案\n" + "\n".join(f"- {f}" for f in fl) +
            "\n# 出处\nunion of `input` keys across public_test_cases/*.json "
            "(obtainable from the Oracle by asking for the test-case files)"))

    # ── T1: routing field value set ──────────────────────────────────────────
    route = detect_route_field(ptc)
    if route:
        field, vals = route
        vl = sorted(vals)
        pat_line = ("\n# 常见错误模式\n" + "\n".join(f"- {p}" for p in pats[:2])
                    if pats else "")
        ids.append(write_question(qdir, adir, qid(),
            {"title": f"routing field '{field}' legal values", "type": "T1",
             "dev": "A", "created": created, "judge": "set_match"},
            f"Name the dispatcher's routing field and list the COMPLETE set of "
            f"its legal values across all public test cases. First line: the "
            f"field name; then one value per line.",
            "# 标准答案\n" + "\n".join([f"- {field}"] + [f"- {v}" for v in vl]) +
            "\n# 出处\nvalues of `" + field + "` across public_test_cases/*.json" +
            pat_line))

    # ── T2: byte-exact stdout per feature (≤4) ───────────────────────────────
    feat_names = sorted(ptc.keys())
    per_feat_pats = {}
    obj = (run_repos.get(alias) or {}).get("objective") or {}
    for suite in ("public_visible", "hidden"):
        s = ((obj.get(suite) or {}).get("sample") or {})
        case = s.get("case") or ""
        stem = case.split("[")[0]
        if stem and s.get("kind") == "mismatch":
            per_feat_pats.setdefault(stem, (s.get("actual") or "").splitlines()[0][:60] if s.get("actual") else None)
    for fname in feat_names:  # T2 覆盖全部 feature（G3 代码对质逐题跑，覆盖面=拦截面）
        spec = ptc[fname]
        cases = spec.get("cases", [])
        if not cases:
            continue
        c0 = cases[0]
        stem = fname[:-5] if fname.endswith(".json") else fname
        wp = per_feat_pats.get(stem)
        pat_line = (f"\n# 常见错误模式\n- {wp}" if wp else "")
        expected_raw = c0.get("expected_output") or ""
        # 字节级答案（base64）：quiz.sh verify 用它与 agent 代码的实际输出做
        # cmp 级比对，免疫 markdown 存储对尾部空白/换行的损耗。
        # 期望为空（沉默契约，如 @043 的空输入边界）也是合法答案，照常编码。
        b64 = base64.b64encode(expected_raw.encode("utf-8")).decode("ascii")
        empty_note = ("NOTE: the expected stdout for this case is EMPTY (zero bytes) — "
                      "silence is the contract. If you believe so, answer with exactly: "
                      "EMPTY\n\n" if expected_raw == "" else "")
        ids.append(write_question(qdir, adir, qid(),
            {"title": f"exact stdout: {stem}", "type": "T2", "dev": "B",
             "created": created, "judge": "byte_equal",
             "expected_b64": b64},
            f"For feature `{stem}`, the dispatcher receives this exact input:\n\n"
            f"```json\n{json.dumps(c0.get('input'), ensure_ascii=False)}\n```\n\n"
            f"{empty_note}"
            f"Write the EXACT complete stdout it must produce — byte-for-byte, "
            f"including exact key names, numeric formats, separators and a "
            f"trailing newline if the expected output has one. Submit only the "
            f"raw output (a fenced block is fine).",
            "# 标准答案\n```\n" + expected_raw + "\n```"
            "\n# 出处\npublic_test_cases/" + fname + " cases[0].expected_output"
            "\n# 判分要点\n逐字节一致；作答包含该完整串也算过" + pat_line))

    # ── T4: conditional oracle cards (≤2) ────────────────────────────────────
    for _, cid, resp, toks in pick_conditional_cards(od.get("hidden_constraints", [])):
        ids.append(write_question(qdir, adir, qid(),
            {"title": f"condition rule {cid}", "type": "T4", "dev": "B",
             "created": created, "judge": "keyword"},
            f"State the COMPLETE conditional rule from Oracle card `{cid}`: "
            f"the exact condition under which each branch applies, and each "
            f"branch's exact output. Include every quoted literal verbatim.",
            "# 标准答案\n" + "\n".join(f"- {t}" for t in toks) +
            f"\n# 出处\noracle card {cid}（向 Oracle 提问可获得）"
            f"\n# 判分要点\n以下每个字面量都必须逐字出现"))

    # ── T6: golden API signature ────────────────────────────────────────────
    sig = od.get("golden_api_signature") or ""
    toks = api_signature_tokens(sig)
    if len(toks) >= 3:
        ids.append(write_question(qdir, adir, qid(),
            {"title": "golden API signature", "type": "T6", "dev": "A",
             "created": created, "judge": "keyword"},
            "Write out the complete golden API signature for this task "
            "(every public entry point with its exact name and parameters, "
            "as the reference implementation defines them).",
            "# 标准答案\n" + "\n".join(f"- {t}" for t in toks) +
            "\n# 出处\noracle_data.golden_api_signature（通过 API 对齐类提问可获得）"
            "\n# 判分要点\n每个签名/参数名都必须出现"))

    stats[alias] = {"questions": n, "ids": ids, "deviation": dev}
    print(f"[{alias}] generated {n} questions -> {out_root / alias}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--aliases", default=",".join(PILOT))
    ap.add_argument("--out", default=str(DEFAULT_OUT))
    args = ap.parse_args()

    run_repos = {}
    if RUN_SETTINGS.is_file():
        run_repos = json.loads(RUN_SETTINGS.read_text(encoding="utf-8")).get("repos", {})

    out_root = Path(args.out)
    stats = {}
    for alias in [a.strip() for a in args.aliases.split(",") if a.strip()]:
        gen_for_alias(alias, out_root, run_repos, stats)
    print(json.dumps({k: v["questions"] for k, v in stats.items()},
                     ensure_ascii=False))


if __name__ == "__main__":
    main()

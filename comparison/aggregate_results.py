#!/usr/bin/env python3
"""Aggregate one ICAE-Bench run into the paper's Table II (main results) format.

Usage:
  python aggregate_results.py <append_id> [--model-label GLM-5.3-Flash] [--split lite]

Reads results/<append_id>/settings.json, aggregates the four metric groups with
the paper's definitions (case-level pass rates; task-level macro means for the
subjective/structural/interaction columns), then merges the resulting row into
comparison/paper_main_results.csv and renders comparison/comparison_table.md.

Only repos with generation == 'success' enter the aggregates — matching the
harness rule that infra/provisioning failures are excluded (retest-eligible),
while model-side failures score 0 and stay.
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent          # comparison/ 的上一级 = ICAE-EVAL
if not (ROOT / "harness").is_dir():
    ROOT = ROOT.parent / "ICAE-EVAL"            # comparison/ 在项目根时
OUT_DIR = Path(__file__).resolve().parent
PAPER_CSV = OUT_DIR / "paper_main_results.csv"

COLS = ["model", "split", "overall", "public", "native", "enhanced",
        "sem", "api", "design", "file", "loc", "cls", "method",
        "constr", "fallback", "budget"]


def _suite(obj: dict, key: str) -> dict:
    s = (obj or {}).get(key) or {}
    return {"passed": s.get("passed") or 0, "total": s.get("total") or 0}


def _mean(vals: list[float]) -> float | None:
    return sum(vals) / len(vals) if vals else None


def _pct(v, nd: int = 1) -> str:
    if v is None or v == "":
        return "—"
    return f"{float(v):.{nd}f}"


def aggregate(append_id: str, label: str, split: str) -> tuple[dict, dict]:
    settings = json.loads((ROOT / "results" / append_id / "settings.json").read_text())
    repos = settings.get("repos", {})

    agg = {"repos_total": len(repos), "repos_ok": 0, "repos_failed": []}
    tp = {"public": 0, "native": 0, "enhanced": 0}
    tt = {"public": 0, "native": 0, "enhanced": 0}
    sem, api, design = [], [], []
    file_r, loc_r, cls_s, mth_s = [], [], [], []
    cov, fb, bud = [], [], []

    for alias, rec in sorted(repos.items()):
        if rec.get("generation") != "success":
            agg["repos_failed"].append(alias)
            continue
        agg["repos_ok"] += 1
        obj = rec.get("objective") or {}
        for key, tier in (("public_visible", "public"), ("hidden", "native"),
                          ("enhanced", "enhanced")):
            s = _suite(obj, key)
            tp[tier] += s["passed"]
            tt[tier] += s["total"]

        ag = rec.get("agentic") or {}
        if ag.get("semantic_similarity") is not None:
            sem.append(ag["semantic_similarity"])
            api.append(ag.get("api_similarity"))
            design.append(ag.get("design_quality"))

        st = rec.get("structural") or {}
        sc = st.get("scale") or {}
        if sc.get("orig_src_files"):
            file_r.append(sc["generated_src_files"] / sc["orig_src_files"] * 100)
        if sc.get("orig_src_loc"):
            loc_r.append(sc["generated_src_loc"] / sc["orig_src_loc"] * 100)
        if st.get("class_similarity") is not None:
            cls_s.append(st["class_similarity"])
        if st.get("method_similarity") is not None:
            mth_s.append(st["method_similarity"])

        it = rec.get("interaction") or {}
        if it.get("ok"):
            cov.append(it["constraint_coverage"])
            fb.append(it["fallback_rate"])
            bud.append(it["budget_usage_rate"])

    overall = ((tp["native"] + tp["enhanced"]) / (tt["native"] + tt["enhanced"]) * 100
               if (tt["native"] + tt["enhanced"]) else None)
    row = {
        "model": label, "split": split,
        "overall": overall,
        "public": tp["public"] / tt["public"] * 100 if tt["public"] else None,
        "native": tp["native"] / tt["native"] * 100 if tt["native"] else None,
        "enhanced": tp["enhanced"] / tt["enhanced"] * 100 if tt["enhanced"] else None,
        "sem": _mean([v for v in sem if v is not None]) if sem else None,
        "api": _mean([v for v in api if v is not None]) if api else None,
        "design": _mean([v for v in design if v is not None]) if design else None,
        "file": _mean(file_r), "loc": _mean(loc_r),
        "cls": _mean(cls_s) if cls_s else None,
        "method": _mean(mth_s) if mth_s else None,
        "constr": _mean(cov), "fallback": _mean(fb), "budget": _mean(bud),
    }
    # 0..1 scales -> 0..100, one decimal, matching the paper tables
    for k in ("sem", "api", "design", "cls", "method"):
        row[k] = round(row[k] * 100, 1) if row[k] is not None else None
    for k in ("overall", "public", "native", "enhanced", "file", "loc",
              "constr", "fallback", "budget"):
        row[k] = round(row[k], 1) if row[k] is not None else None
    return row, agg


def fmt_row(row: dict) -> str:
    keys = ["overall", "public", "native", "enhanced", "sem", "api", "design",
            "file", "loc", "cls", "method", "constr", "fallback", "budget"]
    return " | ".join(_pct(row.get(k)) for k in keys)


def render_md(ours: dict, paper_rows: list[dict], agg: dict, label: str,
              split: str) -> str:
    rows = [r for r in paper_rows if r["split"] == split]
    lite = split == "lite"
    title = ("ICAE-Bench-Lite（50 任务，对应论文 Table II）" if lite
             else "ICAE-Bench 全量（480 任务，对应论文 Table I）")
    lines = [
        f"# 论文主结果格式对比：{label} vs 论文六模型（{title}）",
        "",
        f"- 数据来源：论文 Section IV-B（Table I/II）+ 本地复现 run（append_id 见下方）",
        f"- 本地模型：**{label}**（ark_code 端点，glm-5.3-flash），Claude Code 框架，"
        f"base 环境，fuzzy normal (L1) PRD，DeepSeek-V3.2 键 Oracle（实际为 glm-5.3-flash 路由），"
        f"16 问预算，adaptive thinking",
        f"- 复现规模：{agg['repos_ok']}/{agg['repos_total']} 个任务成功生成并进入统计"
        + (f"（失败：{', '.join(agg['repos_failed'][:8])}…）" if agg["repos_failed"] else ""),
        "",
        "> 论文口径：Overall = (Native 通过数 + Enhanced 通过数) / (Native 总数 + Enhanced 总数)，"
        "case 级聚合；Sem/API/Design/File/LOC/Class/Method/Constr./Fallback/Budget 为任务级宏平均；"
        "File/LOC 为生成/原始比值（%），可超 100；Agentic/主观指标与人类评分仅中等相关（论文自己指出），仅供参考。",
        "",
        "| Model | Overall | Public | Native | Enhanced | Sem. | API | Design | File | LOC | Class | Method | Constr. | Fallback | Budget |",
        "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|",
    ]
    for r in rows:
        cells = fmt_row(r)
        lines.append(f"| {r['model']}（论文） | {cells} |")
    lines.append(f"| **{label}（复现）** | {fmt_row(ours)} |")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("append_id")
    ap.add_argument("--model-label", default="GLM-5.3-Flash")
    ap.add_argument("--split", default="lite", choices=["lite", "full"])
    ap.add_argument("--no-csv", action="store_true",
                    help="do not append the row to paper_main_results.csv")
    a = ap.parse_args()

    row, agg = aggregate(a.append_id, a.model_label, a.split)
    print(json.dumps(row, indent=1))
    print(f"repos ok/total: {agg['repos_ok']}/{agg['repos_total']}",
          f"failed: {agg['repos_failed']}" if agg["repos_failed"] else "")

    paper_rows = list(csv.DictReader(PAPER_CSV.open()))
    OUT_DIR.mkdir(exist_ok=True)
    md = render_md(row, paper_rows, agg, a.model_label, a.split)
    md_path = OUT_DIR / "comparison_table.md"
    md_path.write_text(md)
    print(f"markdown: {md_path}")

    if not a.no_csv:
        ours_csv = OUT_DIR / "glm53flash_results.csv"
        exists = ours_csv.exists()
        with ours_csv.open("a", newline="") as f:
            w = csv.DictWriter(f, fieldnames=COLS)
            if not exists:
                w.writeheader()
            w.writerow(row)
        print(f"csv row appended: {ours_csv}")


if __name__ == "__main__":
    main()

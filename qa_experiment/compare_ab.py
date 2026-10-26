#!/usr/bin/env python3
"""A/B comparison: baseline run vs QA-gate (treatment) run.

Usage:
  python3 qa_experiment/compare_ab.py --treatment <append_id> \
      [--baseline comparison/run_records_5b3b6db7/run_settings.json] \
      [--out comparison/ab_report_<id>.md]

Overall metric follows the paper's aggregate: case-level
(hidden + enhanced) passed / total. Public is shown but excluded from Overall.
"""
import argparse
import json
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
DEFAULT_BASELINE = REPO / "comparison/run_records_5b3b6db7/run_settings.json"

PROTOCOL_ZERO = [f"realcode@{n:03d}" for n in
                 (1, 3, 6, 8, 10, 12, 15, 20, 21, 22, 24, 26, 27, 28,
                  33, 35, 36, 37, 38, 39)]  # §5 的 17 个 + 4 个深度案例中的协议全零仓


def load(path: Path) -> dict:
    d = json.loads(path.read_text(encoding="utf-8"))
    return d.get("repos", {})


def suite(rec: dict, name: str) -> tuple[int, int]:
    s = ((rec or {}).get("objective") or {}).get(name) or {}
    return int(s.get("passed") or 0), int(s.get("total") or 0)


def overall(repos: dict, aliases: list) -> tuple[int, int]:
    p = t = 0
    for a in aliases:
        for s in ("hidden", "enhanced"):
            pp, tt = suite(repos.get(a) or {}, s)
            p += pp
            t += tt
    return p, t


def fmt_pct(p: int, t: int) -> str:
    return f"{100 * p / t:.1f}%" if t else "—"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--treatment", required=True, help="treatment append_id")
    ap.add_argument("--baseline", default=str(DEFAULT_BASELINE))
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    treat_path = REPO / "ICAE-EVAL" / "results" / args.treatment / "settings.json"
    base = load(Path(args.baseline))
    treat = load(treat_path)
    # 只对比真正完成生成+评分的仓：配额中断等 infra error（无 objective 总数）跳过
    aliases = sorted(a for a, r in treat.items() if r.get("objective"))

    lines = [f"# A/B Report — QA-gate treatment `{args.treatment}`",
             f"- baseline: `{Path(args.baseline)}`",
             f"- treatment: `{treat_path}`",
             f"- repos: {len(aliases)}", ""]

    # ── per-repo table ───────────────────────────────────────────────────────
    lines += ["| repo | pub B→T | hidden B→T | enhanced B→T | hid+enh Δ | quiz asked/1st-pass | turns B→T | cost B→T |",
              "|---|---|---|---|---|---|---|---|"]
    for a in aliases:
        b, t = base.get(a) or {}, treat.get(a)
        if not t:
            continue
        cells = []
        delta_he = 0
        for s in ("public_visible", "hidden", "enhanced"):
            bp, bt = suite(b, s)
            tp, tt = suite(t, s)
            cells.append(f"{bp}/{bt} → {tp}/{tt}")
            if s != "public_visible":
                delta_he += tp - bp
        q = t.get("quiz") or {}
        qtxt = (f"{q.get('asked_total')}/{q.get('first_pass_rate')}"
                if q.get("enabled") else "off")
        lines.append(
            f"| {a} | {cells[0]} | {cells[1]} | {cells[2]} | "
            f"{delta_he:+d} | {qtxt} | {b.get('num_turns', '—')}→{t.get('num_turns', '—')} | "
            f"${b.get('cost_usd', 0):.2f}→${t.get('cost_usd', 0):.2f} |")

    # ── aggregates ───────────────────────────────────────────────────────────
    def agg(names, label):
        bp, bt = overall(base, names)
        tp, tt = overall(treat, names)
        lines.append(f"- **{label}** Overall (hidden+enhanced): "
                     f"{fmt_pct(bp, bt)} ({bp}/{bt}) → **{fmt_pct(tp, tt)}** ({tp}/{tt})"
                     f"  Δcases {tp - bp:+d}")
        pub_b = sum(suite(base.get(a) or {}, "public_visible")[0] for a in names)
        pub_t = sum(suite(treat.get(a) or {}, "public_visible")[0] for a in names)
        lines.append(f"  - public passed: {pub_b} → {pub_t}")

    lines += ["", "## Aggregates (case-level)"]
    agg([a for a in aliases if a in treat], "all treatment repos")
    pz = [a for a in PROTOCOL_ZERO if a in treat]
    if pz:
        agg(pz, "protocol-zero subset")

    # ── quiz metrics ─────────────────────────────────────────────────────────
    rows = [(a, treat[a].get("quiz") or {}) for a in aliases if (treat[a].get("quiz") or {}).get("enabled")]
    if rows:
        asked = sum(q.get("asked_total") or 0 for _, q in rows)
        wrong = sum(q.get("wrong_total") or 0 for _, q in rows)
        comp = sum(1 for _, q in rows if q.get("compliance"))
        clean = sum(1 for _, q in rows if q.get("ended_cleanly"))
        lines += ["", "## Quiz metrics (treatment)",
                  f"- compliance: {comp}/{len(rows)} repos ran at least one grade",
                  f"- graded questions: {asked}, first-pass failures: {wrong}",
                  f"- first-pass rate: {fmt_pct(asked - wrong, asked)}",
                  f"- ended cleanly (quiz.sh end): {clean}/{len(rows)}"]

    cost_b = sum((base.get(a) or {}).get("cost_usd") or 0 for a in aliases)
    cost_t = sum((treat.get(a) or {}).get("cost_usd") or 0 for a in aliases)
    turns_b = sum((base.get(a) or {}).get("num_turns") or 0 for a in aliases)
    turns_t = sum((treat.get(a) or {}).get("num_turns") or 0 for a in aliases)
    lines += ["", "## Overhead",
              f"- cost: ${cost_b:.2f} → ${cost_t:.2f} ({cost_t - cost_b:+.2f})",
              f"- turns: {turns_b} → {turns_t} ({turns_t - turns_b:+d})"]

    out = Path(args.out) if args.out else REPO / "comparison" / f"ab_report_{args.treatment}.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))
    print(f"\nwritten: {out}")


if __name__ == "__main__":
    main()

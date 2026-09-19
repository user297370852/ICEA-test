#!/usr/bin/env python3
"""Paper-style figures for the GLM-5.3-Flash ICAE-Bench-Lite reproduction.

Usage: python charts.py <append_id>

Outputs PNGs + a small stats JSON into comparison/figs/.
"""
from __future__ import annotations

import json
import csv
import sys
from collections import defaultdict
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent / "ICAE-EVAL"
OUT = HERE / "figs"
OUT.mkdir(exist_ok=True)

PAPER = {r["model"]: r for r in csv.DictReader((HERE / "paper_main_results.csv").open())}
MODELS_ORDER = ["MiniMax-M2.5", "Claude-Sonnet-4.6", "Gemini-3.1-Pro", "GLM-5.1",
                "Claude-Opus-4.8", "GPT-5.5", "GLM-5.3-Flash"]
PAPER_NAME = "GLM-5.3-Flash"
SHORT = {"Claude-Opus-4.8": "Opus-4.8", "GPT-5.5": "GPT-5.5",
         "Gemini-3.1-Pro": "Gemini-3.1-Pro", "GLM-5.1": "GLM-5.1",
         "Claude-Sonnet-4.6": "Sonnet-4.6", "MiniMax-M2.5": "MiniMax-M2.5",
         "GLM-5.3-Flash": "GLM-5.3-Flash\n(ours)"}
C_PAPER = "#9aa5b1"
C_OURS = "#d62728"

plt.rcParams.update({
    "font.size": 9, "axes.spines.top": False, "axes.spines.right": False,
    "axes.grid": True, "grid.alpha": 0.25, "grid.linewidth": 0.5,
    "figure.dpi": 150, "savefig.bbox": "tight",
})


def load_run(append_id: str) -> dict:
    return json.loads((ROOT / "results" / append_id / "settings.json").read_text())


def ours_suite_rates(repos: dict) -> dict:
    """Case-level suite pass rates over all successful repos."""
    tp = defaultdict(int); tt = defaultdict(int)
    for rec in repos.values():
        if rec.get("generation") != "success":
            continue
        obj = rec.get("objective") or {}
        for key, name in (("public_visible", "public"), ("hidden", "native"), ("enhanced", "enhanced")):
            s = obj.get(key) or {}
            tp[name] += s.get("passed") or 0
            tt[name] += s.get("total") or 0
    return {k: (tp[k] / tt[k] * 100 if tt[k] else None) for k in ("public", "native", "enhanced")}, tp, tt


def ours_overall(repos: dict) -> float | None:
    tp = tt = 0
    for rec in repos.values():
        if rec.get("generation") != "success":
            continue
        obj = rec.get("objective") or {}
        for key in ("hidden", "enhanced"):
            s = obj.get(key) or {}
            tp += s.get("passed") or 0
            tt += s.get("total") or 0
    return tp / tt * 100 if tt else None


# ── Fig 1: main comparison (lite) ────────────────────────────────────────────
def fig1(ours: dict):
    suites = ["overall", "public", "native", "enhanced"]
    labels = ["Overall", "Public", "Native", "Enhanced"]
    x = np.arange(len(suites)); w = 0.11
    fig, ax = plt.subplots(figsize=(7.2, 3.2))
    for i, m in enumerate(MODELS_ORDER):
        if m == PAPER_NAME:
            vals = [ours["agg"].get(s) for s in suites]
            color, hatch, z = C_OURS, None, 3
        else:
            vals = [float(PAPER[m][s]) for s in suites]
            color, hatch, z = C_PAPER, None, 2
        ax.bar(x + (i - 3) * w, vals, w, label=SHORT[m], color=color,
               hatch=hatch, zorder=z, edgecolor="white", linewidth=0.4)
    ax.set_xticks(x); ax.set_xticklabels(labels)
    ax.set_ylabel("Test cases pass rate (%)")
    ax.set_title("ICAE-Bench-Lite main results: paper models (grey) vs our GLM-5.3-Flash run (red)\n"
                 "same protocol: Claude Code, base image, Fuzzy-L1 PRD, Oracle budget 16", fontsize=9)
    ax.legend(ncol=4, fontsize=7.5, frameon=False, loc="upper left")
    ax.set_ylim(0, 78)
    fig.savefig(OUT / "fig1_main_comparison.png")
    plt.close(fig)


# ── Fig 2: per-language Overall ──────────────────────────────────────────────
def fig2(repos: dict, alias_lang: dict):
    tp = defaultdict(int); tt = defaultdict(int); cnt = defaultdict(int)
    for alias, rec in repos.items():
        if rec.get("generation") != "success":
            continue
        lang = alias_lang.get(alias, "?")
        obj = rec.get("objective") or {}
        for key in ("hidden", "enhanced"):
            s = obj.get(key) or {}
            tp[lang] += s.get("passed") or 0
            tt[lang] += s.get("total") or 0
        cnt[lang] += 1
    langs = sorted(tt, key=lambda k: -tp[k] / tt[k] * 100 if tt[k] else 0)
    vals = [tp[l] / tt[l] * 100 for l in langs]
    fig, ax = plt.subplots(figsize=(7.2, 3.0))
    colors = [C_OURS if v >= (ours_overall(repos) or 0) else "#e8888a" for v in vals]
    bars = ax.bar(langs, vals, color=colors, edgecolor="white", linewidth=0.4)
    for b, v, l in zip(bars, vals, langs):
        ax.text(b.get_x() + b.get_width() / 2, v + 1.2, f"{v:.0f}\n(n={cnt[l]})",
                ha="center", va="bottom", fontsize=7)
    line = ours_overall(repos)
    ax.axhline(line, color="#333", lw=0.8, ls="--")
    ax.text(len(langs) - 0.45, line + 1, f"Overall {line:.1f}%", fontsize=7.5, ha="right")
    ax.set_ylabel("Overall pass rate (%)")
    ax.set_title("Per-language Overall pass rate — our GLM-5.3-Flash run (case-level, Lite 50)", fontsize=9)
    ax.set_ylim(0, max(vals) * 1.35)
    fig.savefig(OUT / "fig2_language_breakdown.png")
    plt.close(fig)


# ── Fig 3: failure modes (evaluator-visible, per suite view) ─────────────────
def fig3(repos: dict):
    """Mirror paper's failure-mode taxonomy per suite:
    Clean(all pass) / Mismatch(some output wrong) / Missing(some no-output) /
    Exec(build or runtime error) / No Test(missing test.sh)."""
    modes = ["Clean", "Mismatch", "Missing", "Exec", "No Test"]
    colors = {"Clean": "#4caf50", "Mismatch": "#f39c12", "Missing": "#e67e22",
              "Exec": "#c0392b", "No Test": "#7f8c8d"}
    stats = {v: {"public": 0, "native": 0, "enhanced": 0} for v in modes}
    for rec in repos.values():
        if rec.get("generation") != "success":
            continue
        obj = rec.get("objective") or {}
        for key, view in (("public_visible", "public"), ("hidden", "native"), ("enhanced", "enhanced")):
            s = obj.get(key) or {}
            if s.get("total") and s.get("passed") == s.get("total"):
                m = "Clean"
            elif s.get("reason") == "no_output":
                m = "Exec" if s.get("build_error") else "Missing"
            elif s.get("reason") in ("output_mismatch", "mixed_missing_and_mismatch"):
                m = "Mismatch"
            elif s.get("reason") == "partial_missing_output":
                m = "Missing"
            else:
                m = "Missing"
            stats[m][view] += 1
    views = ["public", "native", "enhanced"]
    x = np.arange(len(views)); bottom = np.zeros(len(views))
    fig, ax = plt.subplots(figsize=(5.6, 3.0))
    for m in modes:
        vals = np.array([stats[m][v] for v in views], dtype=float)
        ax.bar(views, vals, 0.55, bottom=bottom, label=m, color=colors[m],
               edgecolor="white", linewidth=0.5)
        for xi, (v, b) in enumerate(zip(vals, bottom)):
            if v >= 2:
                ax.text(xi, b + v / 2, int(v), ha="center", va="center",
                        fontsize=7.5, color="white", fontweight="bold")
        bottom += vals
    ax.set_ylabel("# repositories")
    ax.set_title("Evaluator-visible outcome per suite view (50 repos)", fontsize=9)
    ax.legend(fontsize=7.5, frameon=False, ncol=2)
    ax.set_ylim(0, 52)
    fig.savefig(OUT / "fig3_failure_modes.png")
    plt.close(fig)
    return stats


# ── Fig 4: constraint coverage vs Overall per repo ───────────────────────────
def fig4(repos: dict):
    xs, ys, sizes = [], [], []
    for rec in repos.values():
        if rec.get("generation") != "success":
            continue
        it = rec.get("interaction") or {}
        obj = rec.get("objective") or {}
        if not it.get("ok"):
            continue
        tp = tt = 0
        for key in ("hidden", "enhanced"):
            s = obj.get(key) or {}
            tp += s.get("passed") or 0
            tt += s.get("total") or 0
        if not tt:
            continue
        xs.append(it["constraint_coverage"]); ys.append(tp / tt * 100)
    r = np.corrcoef(xs, ys)[0, 1] if len(xs) > 2 else float("nan")
    fig, ax = plt.subplots(figsize=(4.6, 3.2))
    ax.scatter(xs, ys, s=26, color=C_OURS, alpha=0.75, edgecolor="white", linewidth=0.4)
    ax.set_xlabel("Constraint coverage (%)")
    ax.set_ylabel("Repo Overall pass rate (%)")
    ax.set_title("More questions answered ≠ better repo\n(per-repo coverage vs Overall, Pearson r=%.2f)" % r, fontsize=9)
    fig.savefig(OUT / "fig4_coverage_vs_overall.png")
    plt.close(fig)
    return r


def main():
    append_id = sys.argv[1]
    alias_map = json.loads((ROOT / "repo_alias.json").read_text())
    alias_lang = {k: v.get("language") for k, v in alias_map.items()}
    run = load_run(append_id)
    repos = run["repos"]
    suites, tp, tt = ours_suite_rates(repos)
    agg = {"overall": ours_overall(repos), **suites}
    stats = {"agg": agg, "cases": {k: {"passed": tp[k], "total": tt[k]} for k in tp}}
    fig1({"agg": agg})
    fig2(repos, alias_lang)
    fm = fig3(repos)
    r = fig4(repos)
    stats["failure_modes"] = fm
    stats["coverage_overall_pearson"] = r
    (OUT / "stats.json").write_text(json.dumps(stats, indent=1))
    print(json.dumps(stats["agg"], indent=1))
    print("figs ->", OUT)


if __name__ == "__main__":
    main()

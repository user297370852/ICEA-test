"""QA-gate experiment support (env-gated via ICAE_QA_MODE=1, default off).

Responsibilities:
  - provision_bank: copy the pre-generated question bank for one task from
    ICAE_QA_BANKS_DIR (default <repo>/qa_banks) to
    results/<append_id>/.qa-bank/<alias>/  — deliberately OUTSIDE the agent's
    working directory so workspace-wide Grep/Glob can never sweep the answers.
    The CLI process gets this path via QA_BANK_DIR (agent_runner.build_env),
    which the plugin hooks and quiz.sh honor.
  - gate_suffix: the task-prompt appendix describing the mandatory self-check
    gates (G1 pre-dispatcher, G3 pre-completion; G2 post-compact comes from the
    plugin's SessionStart hook).
  - harvest_quiz: collect the bank's records into results/<append_id>/quiz/
    and summarize compliance / asked / first-pass for the run settings.
"""
import os
import shutil
from pathlib import Path

from . import config as C

QA_BANKS_DIR = Path(os.environ.get("ICAE_QA_BANKS_DIR",
                                   C.ROOT.parent / "qa_banks"))
GATE_TEMPLATE = C.HARNESS / "prompt_templates" / "qa_gate.md"


def qa_enabled() -> bool:
    return os.environ.get("ICAE_QA_MODE") == "1"


def bank_dir(append_id: str, alias: str) -> Path:
    return C.RESULTS / append_id / ".qa-bank" / alias


def provision_bank(append_id: str, alias: str) -> Path | None:
    """Copy the task's question bank into the run area; None when absent."""
    src = QA_BANKS_DIR / alias
    if not src.is_dir():
        print(f"[{alias}] QA: no question bank at {src} — gate OFF for this repo")
        return None
    dst = bank_dir(append_id, alias)
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src, dst)
    (dst / "records").mkdir(exist_ok=True)
    for name, init in (("stats.tsv", ""), ("history.log", ""),
                       ("wrong-record.md", "# 错题记录\n")):
        p = dst / "records" / name
        if not p.exists():
            p.write_text(init, encoding="utf-8")
    for stale in ("state.env", ".reads"):
        (dst / stale).unlink(missing_ok=True)
    return dst


def gate_suffix(alias: str, append_id: str) -> str:
    if not GATE_TEMPLATE.is_file():
        print("[qa] gate template missing — no gate instructions appended")
        return ""
    text = GATE_TEMPLATE.read_text(encoding="utf-8")
    return "\n\n" + text.format(
        alias=alias,
        quiz_bin=f"../.qa-bank/{alias}/bin/quiz.sh",
        abs_bank=str(bank_dir(append_id, alias)),
    )


def harvest_quiz(append_id: str, alias: str) -> dict:
    """Summarize this task's quiz outcome; archive raw records under quiz/."""
    src = bank_dir(append_id, alias)
    out: dict = {"bank": str(src)}
    if not src.is_dir():
        out["enabled"] = False
        return out
    out["enabled"] = True

    def _read(p: Path) -> str:
        try:
            return p.read_text(encoding="utf-8")
        except FileNotFoundError:
            return ""

    asked = wrong = 0
    for line in _read(src / "records" / "stats.tsv").splitlines():
        parts = line.split("\t")
        if len(parts) >= 3 and parts[0]:
            try:
                asked += int(parts[1] or 0)
                wrong += int(parts[2] or 0)
            except ValueError:
                pass
    records = sum(1 for l in _read(src / "records" / "history.log").splitlines()
                  if l.strip())
    mode = "unknown"
    for line in _read(src / "state.env").splitlines():
        if line.startswith("MODE="):
            mode = line[5:].strip()
    wrong_text = _read(src / "records" / "wrong-record.md")
    out.update({
        "asked_total": asked,
        "wrong_total": wrong,
        "first_pass_rate": round(1 - wrong / asked, 3) if asked else None,
        "grade_records": records,
        "re_pass": wrong_text.count("→ PASS"),
        "re_fail": wrong_text.count("→ FAIL"),
        "compliance": records > 0,
        "ended_cleanly": mode == "IDLE",
    })

    archive = C.RESULTS / append_id / "quiz" / alias
    archive.mkdir(parents=True, exist_ok=True)
    for p in (src / "records" / "stats.tsv", src / "records" / "history.log",
              src / "records" / "wrong-record.md", src / "state.env"):
        if p.is_file():
            try:
                shutil.copy2(p, archive / p.name)
            except OSError:
                pass
    return out

#!/usr/bin/env bash
# self-quiz PreToolUse 守卫（matcher: Write|Edit）
# 职责：自检（quiz）进行中拒绝一切写文件操作——只读考试；超时（>30 分钟）自动作废恢复
# 说明：题库位于 QA_BANK_DIR（实验场景）或 <CLAUDE_PROJECT_DIR>/.qa-bank（交互场景）；
#       出题发生在非考试状态不受影响；判分经 Bash 进行，不受影响
set -u
input=$(cat 2>/dev/null)
ROOT="${CLAUDE_PROJECT_DIR:-$PWD}"
STATE="${QA_BANK_DIR:-$ROOT/.qa-bank}/state.env"
[ -f "$STATE" ] || exit 0

MODE=IDLE; STARTED=0
. "$STATE" 2>/dev/null
[ "${MODE:-IDLE}" = "quiz" ] || exit 0

if [ $(( $(date +%s) - ${STARTED:-0} )) -gt 1800 ]; then
  printf 'MODE=IDLE\nACTIVE=\n' > "$STATE"
  exit 0
fi

echo "自检进行中（只读模式）：答题期间禁止写文件。完成判题并运行 quiz.sh end 后恢复。" >&2
exit 2

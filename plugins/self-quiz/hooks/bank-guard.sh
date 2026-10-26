#!/usr/bin/env bash
# self-quiz PreToolUse 守卫（matcher: Read|Grep|Glob|Bash）
# 职责：① 题库读取拦截——Read/Grep/Glob 的输入涉及题库路径即拒绝（Bash 放行：
#          判分与题库操作经 Bash 进行，这是唯一豁免通道）
#       ② 自检模式读取预算——quiz 状态下 Read/Grep/Glob 计数，超预算拒绝
#       ③ 兜底——bin 同步（会话未重启时）、自检超时作废（>30 分钟）
# 题库位置：QA_BANK_DIR 优先（实验场景），缺省 <CLAUDE_PROJECT_DIR>/.qa-bank（交互场景）
# 输入：stdin 为 hook JSON；exit 0 放行 / exit 2 拒绝（stderr 为拒绝原因）
set -u
input=$(cat 2>/dev/null)

ROOT="${CLAUDE_PROJECT_DIR:-$PWD}"
BANK="${QA_BANK_DIR:-$ROOT/.qa-bank}"
[ -d "$BANK" ] || exit 0

if [ -n "${CLAUDE_PLUGIN_ROOT:-}" ] && [ -d "${CLAUDE_PLUGIN_ROOT}/scripts" ] && [ ! -d "$BANK/bin" ]; then
  mkdir -p "$BANK/bin" 2>/dev/null && cp -R "${CLAUDE_PLUGIN_ROOT}/scripts/." "$BANK/bin/" 2>/dev/null
fi

MODE=IDLE; BUDGET=15; STARTED=0
if [ -f "$BANK/state.env" ]; then
  . "$BANK/state.env" 2>/dev/null
  MODE="${MODE:-IDLE}"; BUDGET="${BUDGET:-15}"; STARTED="${STARTED:-0}"
  if [ "$MODE" = "quiz" ] && [ $(( $(date +%s) - STARTED )) -gt 1800 ]; then
    printf 'MODE=IDLE\nACTIVE=\n' > "$BANK/state.env"
    : > "$BANK/.reads" 2>/dev/null
    MODE=IDLE
  fi
fi

tool=$(printf '%s' "$input" | grep -oE '"tool_name"[[:space:]]*:[[:space:]]*"[^"]*"' | head -1 | sed 's/.*"\([^"]*\)"$/\1/')
[ "$tool" = "Bash" ] && exit 0

# 题库读取拦截：tool_input 指向题库（绝对路径命中题库目录，或含 .qa-bank 相对引用）即拒绝。
# 注意不能按目录 basename 匹配——实验场景题库目录名是任务别名（如 realcode@003），
# 会把工作区自身的全部绝对路径误拦。
if printf '%s' "$input" | grep -qF "$BANK" || printf '%s' "$input" | grep -q '\.qa-bank'; then
  echo "已拦截：$BANK 是自检问答题库，主代理不可读取（防止答案污染）。请按任务要求经 quiz.sh 参加自检。" >&2
  exit 2
fi

# 自检读取预算
if [ "${MODE:-IDLE}" = "quiz" ]; then
  used=$(wc -c < "$BANK/.reads" 2>/dev/null | tr -d '[:space:]')
  used=${used:-0}
  if [ "$used" -ge "$BUDGET" ]; then
    echo "自检读预算（$BUDGET 次 Read/Grep/Glob）已用完：请凭记忆与既有上下文作答并提交判分。" >&2
    exit 2
  fi
  printf 'x' >> "$BANK/.reads"
fi
exit 0

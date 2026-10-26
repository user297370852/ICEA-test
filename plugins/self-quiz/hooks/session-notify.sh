#!/usr/bin/env bash
# self-quiz SessionStart 钩子（startup/resume/clear/compact 均触发）
# 职责：① 幂等同步插件 scripts/ 到题库 bin/（命令与判分脚本经该路径调用）
#       ② 注入规约：compact → 强制自检指令（含具体 bin 路径）；其他来源 → 题库规约
#          （QA_BANK_DIR 已设 = 实验 headless 场景，注入门禁时点文案；否则交互场景文案）
set -u
input=$(cat 2>/dev/null)

BANK="${QA_BANK_DIR:-${CLAUDE_PROJECT_DIR:-}/.qa-bank}"
if [ -n "${CLAUDE_PROJECT_DIR:-}" ] && [ -n "${CLAUDE_PLUGIN_ROOT:-}" ] && [ -d "${CLAUDE_PLUGIN_ROOT}/scripts" ]; then
  mkdir -p "$BANK/bin" 2>/dev/null
  cp -R "${CLAUDE_PLUGIN_ROOT}/scripts/." "$BANK/bin/" 2>/dev/null
fi
BIN="$BANK/bin/quiz.sh"

source=$(printf '%s' "$input" | grep -oE '"source"[[:space:]]*:[[:space:]]*"[^"]*"' | head -1 | sed 's/.*"\([^"]*\)"$/\1/')

if [ "$source" = "compact" ]; then
  ctx="【self-quiz 自检触发】上下文刚被压缩，关键契约细节可能已丢失。立即执行状态重建自检：bash \"$BIN\" start 3 --wrong-only，逐题用 grade 提交作答；答错题须按输出的【复答要求】完成纠偏（复述出处要点并复答）后再继续原任务。若该脚本不存在则忽略本提示。"
elif [ -n "${QA_BANK_DIR:-}" ]; then
  ctx="【self-quiz 已启用（实验模式）】题库目录对主代理不可读（hook 拦截 Read/Grep/Glob；用 Bash 偷看视为作弊）。自检全部经 Bash 调用 \"$BIN\" 完成：start 抽题 → 逐题 heredoc 提交 grade → FAIL 按提示复答 → end 收尾。答题期间写文件被拦（只读），读文件有次数预算。"
else
  ctx="【self-quiz 已启用】.qa-bank/ 为自检问答题库，主代理禁止以任何方式读取其内容（hook 拦截 Read/Grep/Glob；用 Bash 读取视为作弊）。命令：/qa:add 出题（用户意图 + qa-writer 子代理细化）、/qa:quiz [N] [--wrong-only] 抽考、/qa:quiz-k K 按权重取前 K 题、/qa:quiz-all 全量、/qa:stats 统计与错题。"
fi

printf '{"hookSpecificOutput":{"hookEventName":"SessionStart","additionalContext":"%s"}}\n' \
  "$(printf '%s' "$ctx" | sed 's/\\/\\\\/g; s/"/\\"/g')"
exit 0

---
description: 自检考试——抽题（默认 3 题加权随机，支持 N 与 --wrong-only）→ 只读作答 → qa-judge 判题 → FAIL 纠偏循环
argument-hint: [N] [--wrong-only] [--budget M]
---

# /qa:quiz — 自检考试

参数：$ARGUMENTS（为空时默认 3 题）

## 流程（严格按序）

1. **开始**：`bash .qa-bank/bin/quiz.sh start <N> [--wrong-only]`（N 缺省为 3；按上方用户参数拼装）。输出即题面（只含问题，不含答案）。从这一刻起进入考试状态：hook 拦截你的一切 Write/Edit，并限制 Read/Grep/Glob 次数（默认预算 15 次，超预算后凭记忆作答）。
2. **作答**：在回复中逐题作答。规则：
   - 凭当前上下文与记忆作答；可在读预算内查仓库代码取证（鼓励——T2 溯源题必须给出确切出处）；
   - **禁止**访问 .qa-bank（hook 会拦 Read/Grep/Glob；用 Bash 偷看视为作弊，本次自检作废并向用户报告）；
   - 答案具体、可判分：确切的键名/格式/词汇逐字给出；禁止"通常是/大概"式回答；确实不确定就明确写"不确定"，并给最佳推断与依据。
3. **判题**：调用 Agent 工具 spawn `qa-judge`（若列表显示带前缀如 `self-quiz:qa-judge` 则用带前缀名称），prompt 给出逐题的 `QID + 你的作答原文`（原样转交，不要润色）。等待判定。
4. **纠偏循环（仅 FAIL 题，一轮即止）**：对每个 FAIL 题：
   - 认真读 judge 给出的【出处原文】；
   - 在回复中先复述出处要点，再重新作答该题；
   - 再次 spawn qa-judge 只提交复答（它会用 `record --re` 记录）。复答仍 FAIL 则接受结果——错题已在题库中加权，下次抽考会优先出现。
5. **收尾**：`bash .qa-bank/bin/quiz.sh end`（恢复写权限并输出统计），向用户汇总：各题判定、纠偏结果、错题重考安排。

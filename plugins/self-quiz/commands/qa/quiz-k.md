---
description: 自检考试（top-K）——按权重取最该考的 K 题（错次最多、从未考过优先），流程同 /qa:quiz
argument-hint: <K>
---

# /qa:quiz-k — 自检考试（top-K 模式）

K = $ARGUMENTS（为空时默认 5）。

1. 执行 `bash .qa-bank/bin/quiz.sh start <K> --top-k`——按权重排序取前 K 题（weight = 1 + 3×错次 + 从未考过加成），输出即题面。
2. 之后严格按 /qa:quiz 流程执行：只读作答 → spawn qa-judge 判题 → FAIL 纠偏循环 → `quiz.sh end` 收尾并向用户汇总。

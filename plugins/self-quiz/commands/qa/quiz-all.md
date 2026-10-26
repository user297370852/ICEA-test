---
description: 自检考试（全量）——题库全部题目逐题过一遍，流程同 /qa:quiz
---

# /qa:quiz-all — 自检考试（全量）

1. 执行 `bash .qa-bank/bin/quiz.sh start all`——题库全部题目，输出即题面。题量大时注意读预算默认仍为 15 次（可用 `start all --budget M` 调整）。
2. 之后严格按 /qa:quiz 流程执行：只读作答 → spawn qa-judge 判题（可分批 spawn，每批若干题）→ FAIL 纠偏循环 → `quiz.sh end` 收尾并向用户汇总。

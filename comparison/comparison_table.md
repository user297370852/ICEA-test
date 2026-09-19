# 论文主结果格式对比：GLM-5.3-Flash vs 论文六模型（ICAE-Bench-Lite（50 任务，对应论文 Table II））

- 数据来源：论文 Section IV-B（Table I/II）+ 本地复现 run（append_id 见下方）
- 本地模型：**GLM-5.3-Flash**（ark_code 端点，glm-5.3-flash），Claude Code 框架，base 环境，fuzzy normal (L1) PRD，DeepSeek-V3.2 键 Oracle（实际为 glm-5.3-flash 路由），16 问预算，adaptive thinking
- 复现规模：50/50 个任务成功生成并进入统计

> 论文口径：Overall = (Native 通过数 + Enhanced 通过数) / (Native 总数 + Enhanced 总数)，case 级聚合；Sem/API/Design/File/LOC/Class/Method/Constr./Fallback/Budget 为任务级宏平均；File/LOC 为生成/原始比值（%），可超 100；Agentic/主观指标与人类评分仅中等相关（论文自己指出），仅供参考。

| Model | Overall | Public | Native | Enhanced | Sem. | API | Design | File | LOC | Class | Method | Constr. | Fallback | Budget |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Claude-Opus-4.8（论文） | 48.2 | 56.6 | 52.9 | 44.4 | 28.5 | 14.3 | 49.1 | 45.3 | 47.1 | 36.8 | 17.7 | 67.8 | 17.9 | 75.5 |
| GPT-5.5（论文） | 53.3 | 63.8 | 60.9 | 47.4 | 30.0 | 15.2 | 48.7 | 36.8 | 35.0 | 32.6 | 17.7 | 73.2 | 21.0 | 71.7 |
| Gemini-3.1-Pro（论文） | 36.6 | 45.5 | 41.4 | 33.1 | 27.2 | 14.2 | 31.4 | 62.2 | 743.3 | 35.4 | 18.0 | 58.0 | 23.5 | 68.5 |
| GLM-5.1（论文） | 40.0 | 47.6 | 44.5 | 35.9 | 22.6 | 11.0 | 37.9 | 32.4 | 64.5 | 33.2 | 17.4 | 63.3 | 28.4 | 95.4 |
| Claude-Sonnet-4.6（论文） | 40.2 | 47.0 | 44.1 | 37.1 | 34.2 | 16.1 | 44.3 | 33.9 | 51.0 | 34.9 | 18.4 | 60.8 | 25.9 | 75.1 |
| MiniMax-M2.5（论文） | 2.8 | 2.7 | 4.4 | 1.9 | 19.2 | 8.2 | 28.6 | 17.9 | 32.5 | 30.8 | 12.6 | 48.1 | 28.1 | 69.1 |
| **GLM-5.3-Flash（复现）** | 47.1 | 59.3 | 51.0 | 44.2 | 37.4 | 20.3 | 63.0 | 255.5 | 1328.4 | 36.6 | 19.9 | 68.6 | 26.8 | 90.9 |

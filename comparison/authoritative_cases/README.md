# Authoritative Test Cases（Lite 50 · 输入 + 期望输出）

本目录包含 ICAE-Bench-Lite 全部 **50 个任务**的权威黑盒测试用例原文，供失败分析使用。
数据来自官方发布（Zenodo record [21076652](https://zenodo.org/records/21076652) 的
`rcb_tests_repos.tar.gz`，版权归 ICAE-Bench 作者所有），此处仅 redistribution 了 Lite 50 子集。

## 目录结构

```
authoritative_cases/
├── index.json                     # 50 个任务的元数据与每 suite 用例数
└── realcode@NNN/                  # 匿名任务号（对应 run_settings.json 的 repos 键）
    ├── public_test_cases/         # PRD 公开样例（每个 case 可见于需求文档）
    ├── test_cases/                # Native 隐藏用例（由原仓库测试改造）
    └── enhanced_test_cases/       # 增强用例（边界/鲁棒性，合成）
```

每个 `*.json` 文件结构：`{"description": ..., "cases": [{"input": ..., "expected_output": ...}, ...]}`。
`input` 是喂给被测程序（经其自建 dispatcher）的 JSON；`expected_output` 是对 golden 实现逐字节比对的期望 stdout。

## 如何与运行结果关联

- `../run_records_5b3b6db7/run_settings.json` 的 `repos["realcode@NNN"]` 给出每个任务的
  `real_key`（真实仓库名）、`language`、以及 `objective.{public_visible,hidden,enhanced}` 的
  passed/total、粗粒度 `reason` 和一条代表性 `sample`（含 expected/actual）。
- **已知局限（重要）**：run 只记录了每个失败 suite 的**通过数与一条代表样本**，没有记录
  “哪些 case 失败”的逐 case 判定结果；因此本目录无法直接标注失败 case，只能提供全部用例的
  输入与期望输出供对照分析。agent 的实际输出（stdout）与对话轨迹在运行产物清理时未归档，已不可恢复；
  后续 run 会保留并补齐（见 README 第 3 节的 patches 说明）。

## 用例规模

总用例数：Public 815 ｜ Native 1203 ｜ Enhanced 1569（合计 3587，与报告口径一致）。

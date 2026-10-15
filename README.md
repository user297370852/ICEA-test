# ICAE-Bench 复现（macOS · GLM-5.3-Flash）

本仓库是论文 **ICAE-Bench: Evaluating Coding Agents as Interactive Project Builders**
（[arXiv:2607.21217](https://arxiv.org/pdf/2607.21217)，官方仓库 [ALEX-nlp/ICAE-EVAL](https://github.com/ALEX-nlp/ICAE-EVAL)）的**非官方复现记录**：

> 用火山方舟 coding 端点的 **glm-5.3-flash** 作为被测模型，在 **macOS (Apple Silicon) + colima Docker** 上，
> 按论文 IV-B 主实验协议完整复现了 **ICAE-Bench-Lite（50 任务、10 种语言）**，四组指标全部跑通。

> ⚠️ 说明：本机为 **macOS 环境**，与论文的 Linux 参考环境不同；所有平台差异与适配见下文第 3 节。

## 1. 复现结果（速览）

| Model | Overall | Public | Native | Enhanced | Sem. | API | Design | File | LOC | Constr. | Fallback | Budget |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| GPT-5.5（论文） | **53.3** | 63.8 | 60.9 | 47.4 | 30.0 | 15.2 | 48.7 | 36.8 | 35.0 | 73.2 | 21.0 | 71.7 |
| Claude-Opus-4.8（论文） | 48.2 | 56.6 | 52.9 | 44.4 | 28.5 | 14.3 | 49.1 | 45.3 | 47.1 | 67.8 | 17.9 | 75.5 |
| **GLM-5.3-Flash（本仓库复现）** | **47.1** | 59.3 | 51.0 | 44.2 | 37.6 | 20.3 | 63.1 | 255.5 | 1328.4 | 67.8 | 25.8 | 90.7 |
| Claude-Sonnet-4.6（论文） | 40.2 | 47.0 | 44.1 | 37.1 | 34.2 | 16.1 | 44.3 | 33.9 | 51.0 | 60.8 | 25.9 | 75.1 |
| GLM-5.1（论文） | 40.0 | 47.6 | 44.5 | 35.9 | 22.6 | 11.0 | 37.9 | 32.4 | 64.5 | 63.3 | 28.4 | 95.4 |
| Gemini-3.1-Pro（论文） | 36.6 | 45.5 | 41.4 | 33.1 | 27.2 | 14.2 | 31.4 | 62.2 | 743.3 | 58.0 | 23.5 | 68.5 |
| MiniMax-M2.5（论文） | 2.8 | 2.7 | 4.4 | 1.9 | 19.2 | 8.2 | 28.6 | 17.9 | 32.5 | 48.1 | 28.1 | 69.1 |

核心发现（详见 [comparison/GLM-5.3-Flash复现报告.md](comparison/GLM-5.3-Flash复现报告.md)）：

- **Overall 47.1%，居第 3**，与论文第一梯队同量级；较 GLM-5.1 跨代 +7 分；
- 复现了论文核心结论 **"问得多 ≠ 做得对"**（逐仓库约束覆盖率与 Overall 的 Pearson r 仅 0.11）；
- 失分集中在**行为级 mismatch**（50 个仓库全部交付了可运行 test.sh，Exec/No Test 均为 0），
  典型是格式边界（`total=0` vs `total=0.00`）与隐藏接口协议偏离；
- 明显的**过度工程化**倾向：生成代码 LOC 为原仓库的 1328%（七模型中最高）。

| 主结果对比 | 语言分布 |
|---|---|
| ![主结果](comparison/figs/fig1_main_comparison.png) | ![语言分布](comparison/figs/fig2_language_breakdown.png) |
| **失败模式** | **覆盖率 vs 得分** |
| ![失败模式](comparison/figs/fig3_failure_modes.png) | ![覆盖率](comparison/figs/fig4_coverage_vs_overall.png) |

## 2. 仓库结构

```
├── README.md                        ← 本文件
├── 复现状态与操作手册.md              ← 环境搭建 / 运行命令 / 断点续跑 / 踩坑记录
├── models.json.example              ← 本地模型端点配置模板（真实 models.json 含 key，不入库）
├── paper/                           ← 论文中文解读 + arXiv LaTeX 源快照（仅内部使用）
├── ICAE-EVAL/                       ← 官方评测框架完整快照（含本仓库的适配，见 patches/）
│   ├── harness/  user_agent/  scripts/  tools/  images/
│   ├── model_list.json / user_agent/user_model.json  （⚠️ 入库为脱敏占位符版）
│   ├── fuzzy_prds{,_easy,_medium}/  repo_alias.json  user_agent/prd_json*/  ← Oracle 数据
│   ├── rcb_tests_repos/             ← 全部 480 任务的权威测试用例
│   └── .gitignore.upstream-renamed  （上游 .gitignore 改名保留：其原设计是向被测 agent 隐藏上述数据）
├── comparison/                      ← 复现产出
│   ├── GLM-5.3-Flash复现报告.md      ← 完整报告（结果表 + 图 + 失分点分析）
│   ├── comparison_table.md          ├── paper_main_results.csv   （论文 Table I/II 数字）
│   ├── glm53flash_results.csv       ├── figs/（四张图 + stats.json）
│   ├── aggregate_results.py         ├── charts.py                （聚合 / 制图脚本，可复用）
│   ├── run_records_5b3b6db7/        （原始 run 的 settings/summary 备份）
│   └── authoritative_cases/         （Lite 50 全部权威用例：输入+期望输出，3587 个 case）
└── patches/                         ← 对官方 ICAE-EVAL 的本地适配（见第 3 节）
    ├── icae-eval-macos-adaptations.patch
    └── ark-config-example/          （脱敏后的 model_list / user_model 模板，填入自己的 key）
```

**未包含**（GitHub 100MB 单文件硬限制，获取方式见手册）：黄金仓库 `realcode_repos/`（3.2GB，
Zenodo record 21071802）、语言 Docker 镜像 `docker_lang_official/`（按手册 `docker pull` +
`docker save` 重建）、`realcode_repos.tar.lz4`（1.3GB）。

**🔐 安全说明**：所有 API key 均未入库——根目录真实 `models.json` 被排除（仓库内只有
`models.json.example` 脱敏模板）；`ICAE-EVAL/model_list.json` 与 `ICAE-EVAL/user_agent/user_model.json`
入库的是脱敏占位符版本。使用前把占位符替换为自己的 key。

## 3. 复现方法（摘要）

```bash
# 1) 官方代码与数据（详见 复现状态与操作手册.md）
git clone https://github.com/ALEX-nlp/ICAE-EVAL && cd ICAE-EVAL && bash setup.sh

# 2) 应用本仓库的 macOS/模型适配（3 处代码改动，均与评分正确性相关）
git apply /path/to/patches/icae-eval-macos-adaptations.patch
#    a) harness/agentic.py     critic max_tokens 1500→16384、timeout 180s→600s
#       （glm-5.3-flash 默认开启 thinking，会撑爆原值导致 critic 全部超时）
#    b) user_agent/main.py     交互统计兼容 'id'/'constraint_id' 两种字段名的 PRD
# 3) 配置模型端点（ark）：把 patches/ark-config-example/*.json 覆盖到对应位置并填 key
# 4) 跑（macOS 必须 TMPDIR 指到 $HOME 下，colima 默认不挂载 /var/folders）
TMPDIR=$PWD/.tmp_eval ICAE_CLAUDE_CLI="$PWD/.venv/lib/python3.13/site-packages/claude_agent_sdk/_bundled/claude" \
  RUN_LIMIT=50 ./run.sh GLM-5.3-Flash --critic-model-name GLM-5.3-Flash
```

macOS 特有注意事项（完整版见手册）：

1. **Docker**：用 colima；`colima start` 后 daemon 才可用，且重启后需确认；
2. **TMPDIR**：评测的临时暂存目录必须在 `$HOME` 下，否则 `/auth`（注入的权威用例）
   与 `/rcb-out`（输出捕获）挂载为空 → 全部用例判 0 分且无报错，**极易误判为模型 0 分**；
3. **colima 默认只挂载 `$HOME`**：工作区放 `$HOME` 下即可（harness 默认满足）；
4. **Oracle 端口**：多个 run 残留的 Oracle 进程会导致端口占用（uvicorn STARTUP_FAILURE），
   跑前 `pkill -f user_agent/main.py`；
5. Docker Hub 直连不通时，可在 `~/.colima/default/colima.yaml` 配置 registry-mirrors。

## 4. 免责与致谢

- ICAE-Bench 基准、代码与数据集版权归论文作者（复旦 / 美团 / SMU 等）所有，本仓库仅记录复现过程与结果；
- 复现为单次运行，Lite 排名与论文全量排名仅有中等一致性（论文报告 Spearman ρ=0.71），结论解读请以论文为准；
- 感谢官方开源评测框架与数据集。

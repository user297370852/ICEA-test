# qa_experiment — 问答门禁 × ICAE-Bench 实验管线

在 ICAE-EVAL 官方评测 harness（宿主机 Claude CLI + claude-agent-sdk + 容器语言沙箱）上追加
self-quiz 问答门禁，做基线（无门禁）vs 治疗组（门禁）的 A/B 对照。设计依据与理论动机见
[《理解偏差案例库与自检问答设计参考》](../理解偏差案例库与自检问答设计参考.md)；
插件本体见 [plugins/self-quiz](../plugins/self-quiz/README.md)；结果见
[QA 门禁实验报告](../comparison/QA门禁实验报告.md)。

## 管线总览

```text
①  gen_qbank.py      prd_json(public用例+oracle卡) ──生成──> qa_banks/<alias>/{questions,answers}
②  qa_gate.provision_bank          qa_banks/<alias> ──复制──> results/<id>/.qa-bank/<alias>/（工作区外层）
③  agent_runner / orchestrator     注入 --plugin-dir、QA_BANK_DIR、门禁后缀（G1/G2/G3）
④  评测（官方三 suite 逐字节比对）  + quiz 记录归集（compliance/asked/first_pass）
⑤  compare_ab.py                   逐仓与聚合的 A/B 报告（Overall / 协议零分子集 / 开销）
```

全部 harness 改动由环境变量门控（默认关闭，不影响原始复现路径）。

## 文件

| 文件 | 作用 |
|---|---|
| `gen_qbank.py` | 题库生成器。素材白名单：`prd_json` 的 `public_test_cases` + `oracle_data`（hidden_constraints 卡、golden_api_signature）；**enhanced/隐藏 suite 一律不进题库**（防评分集泄漏）。T1 输入字段并集/路由值全集（set_match）、T2 全 feature 逐字节 stdout（byte_equal + `expected_b64`，含空期望"沉默契约"）、T4 条件卡字面量（keyword）、T6 API 签名（keyword）；基线运行的 expected/actual 样本挂为 wrong_answer_pattern |
| `compare_ab.py` | A/B 对比：逐仓 pub/hid/enh、Overall（hidden+enhanced case 级，论文口径）、协议零分仓子集、quiz 指标（合规/首过率）、成本与轮次开销；自动跳过 infra error（无 objective 总数）的仓 |

## 关键 harness 改动（均在 ICAE-EVAL/）

| 文件 | 改动 |
|---|---|
| `harness/creds.py`（新增） | 运行时凭据解析：从 gitignored 的 `models.json` 读 ark_code/AI_Core/Zcode 三段，**构建多渠道端点池**（SUT/Critic：ark plan 主 + Zcode bigmodel anthropic 兜底；Oracle：双后端 round-robin）。被跟踪的 model_list.json / user_model.json 永远保持脱敏占位符 |
| `harness/agent_runner.py` | `ICAE_PLUGIN_DIR` → `plugins` 选项（`--plugin-dir`）；QA 模式透传 `QA_BANK_DIR`/`QA_JUDGE_CONFIG` 进 CLI 进程 |
| `harness/qa_gate.py`（新增） | 题库下发（工作区外层 `.qa-bank/<alias>/`）、门禁后缀渲染（`harness/prompt_templates/qa_gate.md`）、quiz 记录归集与汇总 |
| `harness/orchestrator.py` | QA 预检（插件目录/题库完备性/judge 配置）、per-repo 门禁注入、quiz 汇总入 run settings |
| `harness/prompt_templates/qa_gate.md` | 任务提示后缀：G1（写 dispatcher 前 T1/T2 全过）/ G2（压缩后 wrong-only 清错）/ G3（完成前 T4/T6 清错 + 全部 T2 `verify` 逐字节对质；verify 后改代码必须重验；评测用例只含 input） |
| `run.sh` | 预检接入同一凭据覆盖（避免占位符误拒） |
| `user_agent/user_agent.py` | Oracle 后端池（ark + Zcode，自带 60s 跳过轮换） |

## 运行手册

```bash
# 0) 环境：colima start；凭据在本机 models.json（gitignored，不入库）
# 1) 生成题库（Lite 50）
python3 qa_experiment/gen_qbank.py   # 默认试点 5 仓；--aliases realcode@001,...,realcode@050 全量
# 2) 开跑（QA 模式）
cd ICAE-EVAL
export TMPDIR="$HOME/.tmp"   # colima 不挂载 /var/folders
export ICAE_CLAUDE_CLI="$PWD/.venv/lib/python3.13/site-packages/claude_agent_sdk/_bundled/claude"
export ICAE_QA_MODE=1 ICAE_PLUGIN_DIR=/Users/yeliu/Repository/ICAE/plugins/self-quiz
RUN_LIMIT=50 ./run.sh GLM-5.3-Flash --concurrency 4 --critic-model-name GLM-5.3-Flash
# 3) 配额中断后断点续跑（可多轮；渠道耗尽自动停，恢复后继续）
RUN_LIMIT=50 ./run.sh GLM-5.3-Flash --append-id <id> --resume-fill ...
# 4) 对比
python3 qa_experiment/compare_ab.py --treatment <append_id> \
    [--baseline comparison/run_records_5b3b6db7/run_settings.json]
```

`models.json` 段位职责：`ark_code`（glm-5.3-flash @ ark anthropic 端点，主渠道）、
`Zcode`（glm-5.3-flash @ bigmodel anthropic 端点，兜底渠道）、`AI_Core`（gpt-6.1-sol，
仅 llm_free 判官；判官兜底用 Zcode OpenAI 兼容端点）。

## 运行记录

- 基线：`comparison/run_records_5b3b6db7/`（2026-09，Lite 50，Overall 47.1%）
- 治疗组：`comparison/run_records_3992f153f5bf4d0aa80a27105e752e67/`（settings + summary + 每仓 quiz 判分记录）
- A/B 报告：`comparison/ab_report_*.md`（试点 / 中期 / 终版）
- 题库：`qa_banks/`（50 仓 687 题；由 gen_qbank.py 重新生成，亦可直接复用）

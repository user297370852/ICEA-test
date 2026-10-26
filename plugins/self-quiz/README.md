# self-quiz — 理解偏差自检问答插件

把 ICAE 的 Oracle 机制从"按需讨要、事后评分"改造成"常驻门禁、当场纠错"。设计依据见仓库根目录
[《理解偏差案例库与自检问答设计参考》](../../理解偏差案例库与自检问答设计参考.md)（以下简称"参考文档"）：
题库 = 隐藏约束卡的前移；强制抽考 = 给 HARNESS003"按名讨要"补上强制力；判分 = 持 ground truth 的逐字节对质；
错题本 = 理解偏差画像。完整实验结论见 [QA 门禁实验报告](../../comparison/QA门禁实验报告.md)。

## 角色与数据流

```text
题库 <bank>/                     ── 题面 questions/、标准答案 answers/、记录 records/、quiz.sh
   │  （hook 拦 Read/Grep/Glob；Bash 是唯一豁免通道）
   ├─ 出题（交互场景）  /qa:add 用户出题意图 → 主代理转写上下文摘要 → qa-writer 子代理落成题库文件
   ├─ 出题（实验场景）  qa_experiment/gen_qbank.py 离线生成（只用 public 用例 + oracle 卡，杜绝泄漏）
   ├─ 考试             start 抽题 → 只读作答（读预算计数）→ grade 确定性判分 → FAIL 出示出处 → 复答 → end
   └─ 强制力           PreToolUse hooks：bank-guard 拦题库读取+读预算、quiz-guard 考试期禁写
                       SessionStart：bin 同步 + 规约注入 + compact 后强制自检
```

## 组件

| 路径 | 作用 |
|---|---|
| `commands/qa/{add,quiz,quiz-k,quiz-all,stats}.md` | 交互场景斜杠命令（`/qa:add`、`/qa:quiz [N]`、`/qa:quiz-k K`、`/qa:quiz-all`、`/qa:stats`） |
| `agents/qa-writer.md` `agents/qa-judge.md` | 交互场景的出题/判题子代理（实验场景用确定性脚本判分，不依赖 LLM 判官） |
| `hooks/bank-guard.sh` | 拦截 Read/Grep/Glob 访问题库（绝对路径或 `.qa-bank` 子串命中即拒）；quiz 期间 Read 计数超预算拒绝；Bash 放行 |
| `hooks/quiz-guard.sh` | quiz 状态下拒绝一切 Write/Edit（只读考试）；>30 分钟自动作废防死锁 |
| `hooks/session-notify.sh` | 幂等同步 `scripts/` → `<bank>/bin/`；compact 注入"先自检再继续"；启动注入题库规约 |
| `scripts/quiz.sh` | 题库操作全量：`init / start / grade / verify / record / answer-show / end / stats / state / list` |
| `scripts/judge_llm.py` | 仅 `judge: llm_free` 题使用：AI_Core gpt-6.1-sol 主判 → Zcode glm-5.3-flash 兜底（端点凭据从 `QA_JUDGE_CONFIG` 读取，文件在 gitignored 的 results/ 下，由 harness 生成） |

## 题库文件格式

题面 `questions/QXXX.md`（frontmatter：`id/title/type/deviation_type/created`，正文含输入 JSON 块）：

- `type` 七型：T1 回忆默写 / T2 溯源对质（逐字节 stdout）/ T3 反默认 / T4 边界反面 / T5 配方止损 / T6 枚举对照 / T7 状态重建

答案 `answers/QXXX.md`（判题唯一依据）：

- `judge` 判分类型：`byte_equal`（逐字节；含尾部空白裁剪与"作答包含完整串"容差；**空期望=沉默契约**，答 EMPTY 算对、任何多打内容算错）/ `set_match`（逐项集合，漏项/错拼/多余均不过）/ `keyword`（要点全命中）/ `citation_check`（内容与出处都须对）/ `llm_free`（语义判官）
- `expected_b64`：byte_equal 题的**字节级答案**（base64），`verify` 用它与代码实际输出做 cmp 级比对，免疫 markdown 存储损耗
- 正文四段：标准答案 / 出处（ground_truth_source）/ 判分要点 / 常见错误模式（wrong_answer_pattern，来自基线运行的真实错误输出）

## 关键命令（实验场景，均经 Bash 调用 `<bank>/bin/quiz.sh`）

```bash
quiz.sh start <N|all> [--wrong-only] [--top-k] [--type T1]... [--budget M]  # 抽题并输出题面（无答案）
quiz.sh grade [--re] QXXX <<'EOF' …作答… EOF        # 确定性判分；FAIL 时输出出处原文+复答要求
quiz.sh verify QXXX                                 # 代码对质：跑 agent 自己的 rcb_tests/test.sh，
                                                    # stdout 与 expected_b64 做 cmp 级比对（尾部换行/大小写/格式全暴露）
quiz.sh end                                         # 恢复写权限并输出统计
```

门禁时点：**G1** 写 dispatcher/任何 I-O 代码前（T1+T2 全过）→ **G2** 上下文压缩后（wrong-only 清错）→ **G3**
宣布完成前（T4/T6 清错 + 全部 T2 题 `verify` 逐字节对质）。verify 通过后再改代码必须全部重验。

## 双平台 manifest 兼容（实测踩坑）

Claude CLI（claude-agent-sdk 内置 2.1.273）经 `--plugin-dir` 加载时，`.claude-plugin/plugin.json`
**只允许 name/version/description/author 等元数据字段**——声明 `hooks` 或 `agents` 路径字段会让整个插件
静默拒载（hooks 完全不执行且无任何报错），hooks/commands/agents 一律靠目录自动发现。ZCode 相反，
`.zcode-plugin/plugin.json` 需要显式 `hooks` 字段。因此本插件维护两份 manifest，内容有意不同。

## 环境变量

| 变量 | 作用 |
|---|---|
| `QA_BANK_DIR` | 题库位置（实验场景设为任务工作区外层目录，防全仓 Grep 扫到答案）；缺省 `<cwd>/.qa-bank` |
| `QA_JUDGE_CONFIG` | llm_free 判官端点 JSON（由 `harness/creds.write_judge_config` 从 models.json 生成） |
| `ICAE_PLUGIN_ROOT` / `CLAUDE_PLUGIN_ROOT` | hook 脚本定位（两种运行环境均会注入） |

## 已知边界

- Bash 通道可读题库——防"探索仓库时无意识撞见答案"，不防蓄意作弊（蓄意作弊时测验本身已无意义）。
- `verify` 在 agent 自己的容器里跑，看不到评测的 fresh 容器环境——"verify 后改代码破坏评测协议兼容"
  是已实测的残余盲区（实验报告 §4.3），v0.4 方向是 verify 进 fresh 容器。
- 同题连续 FAIL 无熔断（@049 出现 2407 次判分的死循环），v0.4 加循环熔断。

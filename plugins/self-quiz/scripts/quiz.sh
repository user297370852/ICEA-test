#!/usr/bin/env bash
# self-quiz 题库操作脚本。
# 题库位置：QA_BANK_DIR 优先（实验场景：任务工作区外层的独立目录），
# 缺省为 ${CLAUDE_PROJECT_DIR:-$PWD}/.qa-bank（交互场景：工作目录隐藏文件夹）。
# 运行副本由插件 SessionStart 钩子同步到 <题库>/bin/quiz.sh，主代理与子代理经 Bash 调用。
#
# 用法：
#   quiz.sh init                                              初始化题库（幂等）
#   quiz.sh start <N|all> [--wrong-only] [--top-k] [--type T]... [--budget M]
#                                                            开始自检并输出题面（不含答案）
#   quiz.sh answer-show <QID>                                输出标准答案（判官用）
#   quiz.sh grade [--re] <QID> <<'EOF' ...作答... EOF         确定性判分（作答经 stdin）
#   quiz.sh record [--re] <QID> <PASS|FAIL> -- <说明>         记录判分/复答结果
#   quiz.sh end                                               结束自检（恢复写权限）并输出统计
#   quiz.sh stats                                             统计与错题摘要
#   quiz.sh state                                             当前模式
set -u

ROOT="${CLAUDE_PROJECT_DIR:-$PWD}"
BANK="${QA_BANK_DIR:-$ROOT/.qa-bank}"
QDIR="$BANK/questions"; ADIR="$BANK/answers"; RDIR="$BANK/records"
STATE="$BANK/state.env"; STATS="$RDIR/stats.tsv"
HIST="$RDIR/history.log"; WRONG="$RDIR/wrong-record.md"; READS="$BANK/.reads"
BUDGET_DEFAULT=15
BIN_DIR="$BANK/bin"

die() { echo "ERROR: $*" >&2; exit 1; }
now_epoch() { date +%s; }

load_state() {
  MODE=IDLE; ACTIVE=""; BUDGET=$BUDGET_DEFAULT; STARTED=0
  [ -f "$STATE" ] && . "$STATE" 2>/dev/null
  MODE="${MODE:-IDLE}"; ACTIVE="${ACTIVE:-}"
  BUDGET="${BUDGET:-$BUDGET_DEFAULT}"; STARTED="${STARTED:-0}"
}

expire_stale() {
  load_state
  if [ "$MODE" = "quiz" ] && [ $(( $(now_epoch) - STARTED )) -gt 1800 ]; then
    printf 'MODE=IDLE\nACTIVE=\n' > "$STATE"; : > "$READS" 2>/dev/null
    MODE=IDLE; ACTIVE=""
  fi
}

list_ids() { ls "$QDIR" 2>/dev/null | sed -n 's/\.md$//p' | sort; }

fm_field() { # fm_field <file> <key>：读 frontmatter 字段值
  awk -v k="$2" '
    NR == 1 && /^---[[:space:]]*$/ { fm = 1; next }
    fm && /^---[[:space:]]*$/ { exit }
    fm && index($0, k ":") == 1 { sub("^" k ":[ ]*", ""); print; exit }
  ' "$1"
}

strip_fm() { # 去掉 frontmatter，输出正文
  awk 'NR == 1 && /^---[[:space:]]*$/ { fm = 1; next }
       fm && /^---[[:space:]]*$/ { fm = 0; next }
       fm == 0 { print }' "$1"
}

section() { # section <file> <标题词>：提取 markdown 中 `# <标题>` 到下一个 `# ` 之间正文
  awk -v t="$2" '
    BEGIN { want = 0 }
    /^#[^#]/ {
      h = $0; sub(/^#[ ]*/, "", h)
      if (want) { exit }
      want = (index(h, t) == 1)
      next
    }
    want { print }
  ' "$1"
}

strip_fence() { # 去掉首尾 ``` 围栏行并裁剪首尾空白
  awk 'NR==1 && /^```/ { fence=1; next} fence && /^```/ {fence=0; next} {print}' | sed '/./,$!d' | awk '{lines[NR]=$0} END {for(i=NR;i>=1;i--){if(lines[i]~/[^[:space:]]/){last=i;break}} for(i=1;i<=last;i++) print lines[i]}'
}

make_pool() { # make_pool <all|wrong> [类型csv，如 T1,T2]：输出 "ID weight"
  local types="${2:-}"
  { for id in $(list_ids); do
      local t; t=$(fm_field "$QDIR/$id.md" type)
      if [ -n "$types" ]; then
        case ",$types," in *",$t,"*) ;; *) continue ;; esac
      fi
      echo "$id"
    done
    printf '\n__STATS__\n'; cat "$STATS" 2>/dev/null; } | awk -v f="$1" '
    /^__STATS__$/ { ins = 1; next }
    !ins && NF { ids[++n] = $1 }
    ins && NF { st[$1] = $2 " " $3 }
    END {
      for (i = 1; i <= n; i++) {
        id = ids[i]; asked = 0; wrong = 0
        if (id in st) { split(st[id], a, " "); asked = a[1] + 0; wrong = a[2] + 0 }
        if (f == "wrong" && wrong == 0) continue
        printf "%s %d\n", id, 1 + 3 * wrong + (asked == 0 ? 2 : 0)
      }
    }'
}

sample_n() { # 加权无放回抽样：stdin "ID weight" →  stdout 最多 N 个 ID
  awk -v n="$1" 'BEGIN { srand() }
    { id[NR] = $1; w[NR] = $2; total += $2 }
    END {
      k = (n < NR ? n : NR)
      for (c = 1; c <= k; c++) {
        r = rand() * total
        for (i = 1; i <= NR; i++) {
          if (used[i]) continue
          r -= w[i]
          if (r <= 0) { print id[i]; used[i] = 1; total -= w[i]; break }
        }
      }
    }'
}

cmd_init() {
  mkdir -p "$QDIR" "$ADIR" "$RDIR"
  [ -f "$STATS" ] || : > "$STATS"
  [ -f "$HIST" ] || : > "$HIST"
  [ -f "$WRONG" ] || printf '# 错题记录（判分时追加；内容已在纠偏时向主代理出示）\n' > "$WRONG"
  # 仅当题库位于某个 git 工作区内时追加 .gitignore（实验场景题库在 results/ 下，本就忽略）
  if [ -z "${QA_BANK_DIR:-}" ] && git -C "$ROOT" rev-parse --git-dir >/dev/null 2>&1; then
    grep -qxF '.qa-bank/' "$ROOT/.gitignore" 2>/dev/null || printf '\n.qa-bank/\n' >> "$ROOT/.gitignore"
  fi
  echo "题库已就绪：${BANK}（questions / answers / records）"
}

cmd_start() {
  local n="${1:-3}"; [ $# -gt 0 ] && shift
  [ "$n" = "all" ] || [[ "$n" =~ ^[0-9]+$ ]] || die "题目数量 N 必须是正整数或 all"
  local filter=all topk=0 budget=$BUDGET_DEFAULT types=""
  while [ $# -gt 0 ]; do
    case "$1" in
      --wrong-only) filter=wrong ;;
      --top-k) topk=1 ;;
      --type) types="${types:+$types,}${2:?--type 需要题型}"; shift ;;
      --budget) budget="${2:?--budget 需要数值}"; shift ;;
      *) die "未知参数：$1" ;;
    esac
    shift
  done
  expire_stale
  [ -d "$QDIR" ] || die "题库不存在，先运行 quiz.sh init"
  rm -f "$RDIR"/.circuit_* "$RDIR"/.fails_* 2>/dev/null  # 新一轮自检重置熔断
  local sel
  if [ "$n" = "all" ]; then
    sel=$(make_pool "$filter" "$types" | cut -d' ' -f1)
  elif [ "$topk" = "1" ]; then
    sel=$(make_pool "$filter" "$types" | sort -k2,2nr | head -n "$n" | cut -d' ' -f1)
  else
    sel=$(make_pool "$filter" "$types" | sample_n "$n")
  fi
  [ -n "$sel" ] || die "没有可抽的题目（题库为空或过滤后为空）"
  local count; count=$(printf '%s\n' "$sel" | grep -c .)
  printf 'MODE=quiz\nACTIVE="%s"\nBUDGET=%s\nSTARTED=%s\n' "$sel" "$budget" "$(now_epoch)" > "$STATE"
  : > "$READS"
  echo "=== 自检开始：共 $count 题（答题期间只读；读预算 $budget 次 Read/Grep/Glob）==="
  local i=0 id
  for id in $sel; do
    i=$((i + 1))
    echo
    echo "── [$i/$count] ${id}（$(fm_field "$QDIR/$id.md" type)）──"
    strip_fm "$QDIR/$id.md" | sed '/./,$!d'
  done
  echo
  echo "（作答：逐题用 heredoc 提交判分，如：bash \"$BIN_DIR/quiz.sh\" grade Q001 <<'EOF' …你的答案… EOF）"
}

cmd_answer_show() {
  local id="$1"
  [ -f "$ADIR/$id.md" ] || die "答案不存在：$id"
  cat "$ADIR/$id.md"
}

# ── 确定性判分 ────────────────────────────────────────────────────────────────

_norm_text() { strip_fence; }

_parse_items() { # 逐项集合：stdin 多行文本 → 每行一项（去 "- " 前缀/空白）
  sed 's/^[[:space:]]*[-*•][[:space:]]*//' | awk 'NF{print}' | sed 's/^[[:space:]]*//;s/[[:space:]]*$//'
}

_ans_items() { # 作答解析：按换行/逗号/顿号/分号切分
  tr '，、;；' '\n\n\n\n' | sed 's/,/\n/g' | _parse_items | tr -d "\"'" | sort -u
}

_grade_byte_equal() { # $1=expected $2=answer → 设置 pass/diff_desc
  local exp ans; exp=$(printf '%s' "$1" | _norm_text); ans=$(printf '%s' "$2" | _norm_text)
  if [ -z "$exp" ]; then
    # 沉默契约：golden 期望零字节输出。作答为空、EMPTY、(empty) 均算对；
    # 任何实际内容（如多打的 0.000000）都算错。
    case "$(printf '%s' "$ans" | tr '[:upper:]' '[:lower:]')" in
      ""|empty|"（empty）"|"（空）"|"（空输出）"|"（沉默）"|"（无输出）")
        pass=1; diff_desc="沉默契约正确：期望为空输出" ;;
      *)
        pass=0; diff_desc="golden 期望为空输出（零字节，沉默即契约），但作答有内容「${ans:0:40}」" ;;
    esac
    return
  fi
  if [ "$exp" = "$ans" ]; then
    pass=1; diff_desc="逐字节一致"
  elif [[ -n "$exp" && "$ans" == *"$exp"* ]]; then
    pass=1; diff_desc="作答包含逐字节正确的期望输出"
  else
    pass=0
    local pos=0 i=1 c1 c2 off
    local elen=${#exp} alen=${#ans}
    local max=$elen
    [ "$alen" -gt "$max" ] && max=$alen
    while [ "$i" -le "$max" ]; do
      c1=${exp:$((i - 1)):1}; c2=${ans:$((i - 1)):1}
      if [ "$c1" != "$c2" ]; then pos=$i; break; fi
      i=$((i + 1))
    done
    [ "$pos" -eq 0 ] && pos=$((max + 1))
    off=$((pos > 1 ? pos - 1 : 0))
    diff_desc="第 ${pos} 字符起不一致：标准「${exp:$off:24}」vs 作答「${ans:$off:24}」"
  fi
}

_grade_set_match() {
  local exp ans; exp=$(printf '%s' "$1" | _parse_items | sort -u); ans=$(printf '%s' "$2" | _ans_items)
  local miss extra
  miss=$(comm -23 <(printf '%s\n' "$exp") <(printf '%s\n' "$ans" | sed '/^$/d') | tr '\n' ' ')
  extra=$(comm -13 <(printf '%s\n' "$exp") <(printf '%s\n' "$ans" | sed '/^$/d') | tr '\n' ' ')
  if [ -z "$miss" ] && [ -z "$extra" ]; then
    pass=1; diff_desc="集合完全一致"
  else
    pass=0
    diff_desc="缺失项: ${miss:-无}；多余/错拼项: ${extra:-无}"
  fi
}

_grade_keyword() {
  local ans="$2" missing=""
  local kw
  while IFS= read -r kw; do
    [ -z "$kw" ] && continue
    case "$ans" in *"$kw"*) ;; *) missing="$missing $kw" ;; esac
  done <<EOF
$(printf '%s' "$1" | _parse_items)
EOF
  if [ -z "${missing// /}" ]; then
    pass=1; diff_desc="全部要点命中"
  else
    pass=0; diff_desc="未命中的必要要点:${missing}"
  fi
}

_grade_citation_check() { # 标准答案段格式：内容: X / 出处: Y（两行）
  local ans="$2" phrase src
  phrase=$(printf '%s' "$1" | sed -n 's/^[[:space:]]*内容[[:space:]]*:[[:space:]]*//p')
  src=$(printf '%s' "$1" | sed -n 's/^[[:space:]]*出处[[:space:]]*:[[:space:]]*//p')
  [ -z "$phrase" ] && { phrase=$(printf '%s' "$1" | head -1); }
  local srcseg="${src##*/}"
  local ok_c=0 ok_s=0
  case "$ans" in *"$phrase"*) ok_c=1 ;; esac
  case "$ans" in *"$src"*) ok_s=1 ;; esac
  [ -z "$src" ] && ok_s=1
  [ "$ok_c" = 1 ] && [ "$ok_s" = 0 ] && case "$ans" in *"$srcseg"*) ok_s=1 ;; esac
  if [ "$ok_c" = 1 ] && [ "$ok_s" = 1 ]; then
    pass=1; diff_desc="内容与出处均正确"
  else
    pass=0
    diff_desc="内容[$([ $ok_c = 1 ] && echo 对 || echo 错)] 出处[$([ $ok_s = 1 ] && echo 对 || echo 错)]；要求内容含「${phrase}」且出处含「${src}」"
  fi
}

cmd_grade() {
  local re=0
  if [ "${1:-}" = "--re" ]; then re=1; shift; fi
  local id="${1:?用法: quiz.sh grade [--re] <QID>，作答经 stdin 传入}"
  [ -f "$ADIR/$id.md" ] || die "答案不存在：$id"
  # 熔断（v0.4）：同题连续 3 次判分 FAIL 后跳过，防死循环（如 @049 的 2407 次判分）；
  # --re 复答不受熔断限制（它是恢复路径，通过即清除熔断）；新 start 重置全部熔断
  local circ="$RDIR/.circuit_$id"
  if [ -f "$circ" ] && [ "$re" = "0" ]; then
    echo "──────── $id SKIPPED（已熔断：此前连续多次未通过，判分跳过；接受结果并继续后续流程，新一次 start 会重置）"
    exit 0
  fi
  local ans judge expected src pass=0 diff_desc=""
  ans=$(cat)
  judge=$(fm_field "$ADIR/$id.md" judge)
  expected=$(section "$ADIR/$id.md" "标准答案")
  src=$(section "$ADIR/$id.md" "出处")
  case "$judge" in
    byte_equal)     _grade_byte_equal "$expected" "$ans" ;;
    set_match)      _grade_set_match "$expected" "$ans" ;;
    keyword)        _grade_keyword "$expected" "$ans" ;;
    citation_check) _grade_citation_check "$expected" "$ans" ;;
    llm_free)
      local tmp="$RDIR/.ans_$id.tmp"
      printf '%s' "$ans" > "$tmp"
      local out
      out=$(python3 "$BIN_DIR/judge_llm.py" --question "$QDIR/$id.md" \
            --expected "$ADIR/$id.md" --answer "$tmp" 2>&1)
      rm -f "$tmp"
      case "$out" in
        PASS*) pass=1; diff_desc="LLM 判官通过：${out#PASS}" ;;
        FAIL*) pass=0; diff_desc="LLM 判官否决：${out#FAIL}" ;;
        *) echo "ERROR: 判官不可用：$out"; exit 3 ;;
      esac ;;
    *) die "未知 judge 类型：$judge" ;;
  esac

  local verdict=FAIL; [ "$pass" = 1 ] && verdict=PASS
  # 熔断计数：连续 FAIL 计数，PASS 或复答通过即清零；第 3 次 FAIL 触发熔断
  local failfile="$RDIR/.fails_$id"
  if [ "$pass" = 1 ]; then
    rm -f "$failfile" "$circ"
  elif [ "$re" = "0" ]; then
    local n; n=$(( $(cat "$failfile" 2>/dev/null || echo 0) + 1 ))
    printf '%s' "$n" > "$failfile"
    if [ "$n" -ge 3 ]; then printf '1' > "$circ"; fi
  fi
  # 复用 record 的统计/错题逻辑
  _record_result "$re" "$id" "$verdict" "判分(${judge})：${diff_desc}；作答摘要：$(printf '%s' "$ans" | tr '\n' ' ' | cut -c1-200)"

  echo "──────── $id ${verdict}（${judge}）"
  echo "【判定】$diff_desc"
  echo "【你的作答】$(printf '%s' "$ans" | tr '\n' ' ' | cut -c1-200)"
  if [ "$pass" = 0 ]; then
    echo "【出处原文】$src"
    echo "【标准答案要点】$(printf '%s' "$expected" | tr '\n' ' ' | cut -c1-300)"
    echo "【复答要求】先复述上方出处要点，再重新提交：bash \"${BIN_DIR}/quiz.sh\" grade --re $id <<'EOF' …复答… EOF"
  fi
}

_record_result() { # 与 cmd_record 相同的落库逻辑（grade 内部调用）
  local re="$1" id="$2" res="$3" note="$4"
  local stamp; stamp=$(date '+%F %T')
  local asked=0 wrong=0 row
  row=$(awk -F'\t' -v q="$id" '$1 == q { print $2 "\t" $3 }' "$STATS" 2>/dev/null)
  if printf '%s' "$row" | grep -qE '^[0-9]+[[:space:]]*[0-9]+$'; then
    asked=${row%%$'\t'*}; wrong=${row##*$'\t'}
  fi
  [ "$re" = "0" ] && { asked=$((asked + 1)); [ "$res" = "FAIL" ] && wrong=$((wrong + 1)); }
  local tmp="$STATS.tmp" now; now=$(now_epoch)
  awk -F'\t' -v OFS='\t' -v q="$id" -v a="$asked" -v w="$wrong" -v r="$res" -v t="$now" '
    $1 == q { $2 = a; $3 = w; $4 = r; $5 = t; print; found = 1; next }
    { print }
    END { if (!found) print q, a, w, r, t }' "$STATS" > "$tmp" && mv "$tmp" "$STATS"
  local mark="$res"; [ "$re" = "1" ] && mark="$res(re)"
  printf '%s\t%s\t%s\t%s\n' "$stamp" "$id" "$mark" "${note:0:400}" >> "$HIST"
  if [ "$res" = "FAIL" ] && [ "$re" = "0" ]; then
    { printf '\n## %s · %s · FAIL\n\n%s\n' "$stamp" "$id" "$note"; } >> "$WRONG"
  elif [ "$re" = "1" ]; then
    printf -- '- %s 复答 %s → %s\n' "$stamp" "$id" "$res" >> "$WRONG"
  fi
}

cmd_record() {
  local re=0
  if [ "${1:-}" = "--re" ]; then re=1; shift; fi
  [ $# -ge 2 ] || die "用法: quiz.sh record [--re] <QID> <PASS|FAIL> -- <说明>"
  local id="$1" res="$2"; shift 2
  [ "${1:-}" = "--" ] && shift
  _record_result "$re" "$id" "$res" "$*"
  local mark="$res"; [ "$re" = "1" ] && mark="$res(re)"
  echo "已记录：$id $mark"
}

cmd_list() { # list [--type T]：列出（可按题型过滤的）题号
  local types=""
  while [ $# -gt 0 ]; do
    case "$1" in
      --type) types="${types:+$types,}${2:?--type 需要题型}"; shift ;;
      *) die "未知参数：$1" ;;
    esac
    shift
  done
  local id t
  for id in $(list_ids); do
    if [ -n "$types" ]; then
      t=$(fm_field "$QDIR/$id.md" type)
      case ",$types," in *",$t,"*) echo "$id" ;; esac
    else
      echo "$id"
    fi
  done
}

cmd_verify() { # 代码对质（仅 byte_equal/T2 题）：跑 agent 自己的 rcb_tests/test.sh，
  # 将代码实际输出与 golden 逐字节比对（cmp 级，尾部换行/大小写/格式差异都会暴露）
  local id="${1:?用法: quiz.sh verify <QID>}"
  [ -f "$ADIR/$id.md" ] || die "答案不存在：$id"
  local judge b64
  judge=$(fm_field "$ADIR/$id.md" judge)
  [ "$judge" = "byte_equal" ] || { echo "skip：$id 不是 byte_equal 题（${judge}）"; exit 0; }
  grep -q '^expected_b64:' "$ADIR/$id.md" || die "$id 缺 expected_b64 字段（旧格式题库，请用 gen_qbank.py 重新生成）"
  b64=$(fm_field "$ADIR/$id.md" expected_b64)
  [ -f rcb_tests/test.sh ] || die "rcb_tests/test.sh 不存在——先完成实现再代码对质"
  local stem
  stem=$(section "$ADIR/$id.md" "出处" | sed -n 's#.*/\([^/.]*\)\.json.*#\1#p' | head -1)
  [ -n "$stem" ] || die "无法从出处解析 feature 名"
  local vname="qa_verify_$id"
  mkdir -p "rcb_tests/$vname" "rcb_tests/stdout/$vname"
  python3 - "$QDIR/$id.md" "rcb_tests/$vname/$stem.json" <<'PY' || die "构造对质用例失败（题面无输入 JSON 块）"
import json, re, sys
q = open(sys.argv[1], encoding="utf-8").read()
m = re.search(r"```json\n(.*?)\n```", q, re.S)
if not m:
    raise SystemExit(1)
case = {"description": "self-quiz code verification", "cases": [{"input": json.loads(m.group(1))}]}
open(sys.argv[2], "w", encoding="utf-8").write(json.dumps(case, ensure_ascii=False))
PY
  # ── 执行对质：优先 fresh 容器（v0.4，完全模拟评测协议：同镜像、用例仅含 input、
  #    干净环境）；无 QA_AGENT_CONTAINER/docker 时退回本机原地执行
  local out=""
  if [ -n "${QA_AGENT_CONTAINER:-}" ] && command -v docker >/dev/null 2>&1 \
     && docker inspect "${QA_AGENT_CONTAINER}" >/dev/null 2>&1; then
    local img
    img=$(docker inspect "${QA_AGENT_CONTAINER}" --format '{{.Config.Image}}')
    rm -rf "rcb_tests/qa_verify_f" "rcb_tests/stdout/qa_verify_f"
    docker run --rm -v "$PWD:/gen" -v "$PWD/rcb_tests/$vname:/auth:ro" -w /gen "$img" \
      bash -c 'mkdir -p rcb_tests/qa_verify_f && cp -r /auth/. rcb_tests/qa_verify_f/ \
               && bash rcb_tests/test.sh --cases-dir qa_verify_f' >/dev/null 2>&1
    out=$(ls "rcb_tests/stdout/qa_verify_f/$stem"@*.txt 2>/dev/null | head -1)
    echo "（fresh 容器对质：镜像 ${img}，用例仅含 input——与评测协议同构）"
  else
    bash rcb_tests/test.sh --cases-dir "$vname" >/dev/null 2>&1
    out=$(ls "rcb_tests/stdout/$vname/$stem"@*.txt 2>/dev/null | head -1)
  fi
  local expf="$BANK/.verify_exp.tmp"
  printf '%s' "$b64" | base64 -d > "$expf"
  local note
  if [ -n "$out" ] && cmp -s "$expf" "$out"; then
    note="代码对质：$stem 实际输出与 golden 逐字节一致"
    printf '%s\t%s\tVERIFY-PASS\t%s\n' "$(date '+%F %T')" "$id" "$note" >> "$HIST"
    echo "──────── $id VERIFY PASS（${stem}）：代码输出与 golden 逐字节一致"
  elif [ -z "$out" ]; then
    note="代码对质：$stem 在评测协议下未产出任何输出（test.sh 失败或 runner 依赖了评测不提供的内容，"
    note="${note}如 case 里的 expected_output 字段、未在 test.sh 内引导的依赖）——评测将记 0，必须修复"
    printf '%s\t%s\tVERIFY-FAIL\t%s\n' "$(date '+%F %T')" "$id" "$note" >> "$HIST"
    echo "──────── $id VERIFY FAIL（${stem}）：评测协议下零输出"
    echo "【修复要求】1) test.sh 必须自带依赖引导（fresh 容器无你手工安装过的东西）；"
    echo "2) runner 不得读取评测用例中不存在的字段（用例只含 input）；"
    echo "3) 在本机自查通过后，用本命令重跑直到 VERIFY PASS。"
  else
    local where; where=$(cmp "$expf" "$out" 2>&1 | head -1)
    note="代码对质：$stem 不一致（${where}）——必须修代码与自建用例"
    printf '%s\t%s\tVERIFY-FAIL\t%s\n' "$(date '+%F %T')" "$id" "$note" >> "$HIST"
    echo "──────── $id VERIFY FAIL（${stem}）"
    echo "【差异】${where}（格式：字节/行号 char/line）"
    echo "【golden 期望】$(head -c 200 "$expf" | cat -v)$([ $(wc -c < "$expf") -gt 200 ] && echo '…')"
    echo "【代码实际】$(head -c 200 "$out" | cat -v)$([ $(wc -c < "$out") -gt 200 ] && echo '…')"
    echo "【修复要求】修正 dispatcher/test.sh 的输出字节（注意：尾部换行有无、字母大小写、数字格式、行序），"
    echo "并同步修正你的自建 public_test_cases（以 golden 为准，而不是以你的输出为准）；改完重跑本命令直到 PASS。"
  fi
  rm -f "$expf"
}

cmd_end() {
  expire_stale
  printf 'MODE=IDLE\nACTIVE=\n' > "$STATE"
  : > "$READS" 2>/dev/null
  echo "自检结束，写权限已恢复。当前统计："
  cmd_stats
}

cmd_stats() {
  [ -d "$QDIR" ] || die "题库不存在，先运行 quiz.sh init"
  echo "== 题库统计（不含标准答案）=="
  local id asked wrong last title type row
  for id in $(list_ids); do
    row=$(awk -F'\t' -v q="$id" '$1 == q { print $2 "\t" $3 "\t" $4 }' "$STATS" 2>/dev/null)
    if [ -n "$row" ]; then IFS=$'\t' read -r asked wrong last <<< "$row"; else asked=0; wrong=0; last=-; fi
    title=$(fm_field "$QDIR/$id.md" title)
    type=$(fm_field "$QDIR/$id.md" type)
    printf '%-6s %-5s 考%-3s 错%-3s 最近:%-5s %s\n' "$id" "[$type]" "$asked" "$wrong" "$last" "${title:-（无标题）}"
  done
  echo
  echo "== 错题记录（最近）=="
  tail -n 25 "$WRONG" 2>/dev/null
}

cmd_state() { load_state; echo "MODE=$MODE ACTIVE='$ACTIVE' BUDGET=$BUDGET"; }

case "${1:-help}" in
  init) shift; cmd_init "$@" ;;
  start) shift; cmd_start "$@" ;;
  answer-show) shift; [ $# -ge 1 ] || die "用法: quiz.sh answer-show <QID>"; cmd_answer_show "$@" ;;
  grade) shift; cmd_grade "$@" ;;
  verify) shift; cmd_verify "$@" ;;
  list) shift; cmd_list "$@" ;;
  record) shift; cmd_record "$@" ;;
  end) shift; cmd_end "$@" ;;
  stats) shift; cmd_stats "$@" ;;
  state) shift; cmd_state "$@" ;;
  *) sed -n '2,16p' "$0" ;;
esac

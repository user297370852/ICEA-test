## Mandatory Self-Check Gates (comprehension QA)

This task is instrumented with a comprehension self-check system. A per-task question bank exists at `{abs_bank}` — you CANNOT read it (file reads of the bank are blocked; circumventing the block via shell counts as cheating and voids the run). All quiz operations go through `{quiz_bin}`.

**Gate G1 — BEFORE writing the dispatcher / runner / any input-output plumbing** (`rcb_tests/dispatcher*`, `test.sh` I/O handling), complete a contract self-check and clear every question:

```bash
bash {quiz_bin} start 5 --type T1 --type T2
```

The command prints the selected questions (no answers). For each listed QID, submit your answer through stdin (only the raw answer — a fenced block is fine):

```bash
bash {quiz_bin} grade QID <<'EOF'
your exact answer here
EOF
```

A FAIL prints the authoritative source excerpt (ground truth). Restate that source in your own words, fix your understanding, then resubmit once with `bash {quiz_bin} grade --re QID <<'EOF' ... EOF`. After all questions are judged:

```bash
bash {quiz_bin} end
```

**Gate G2 — after any context compaction** (a system reminder will appear): run `bash {quiz_bin} start 3 --wrong-only` and clear failures the same way, then `end`.

**Gate G3 — BEFORE declaring the task complete**, two parts:

(a) `bash {quiz_bin} start 5 --type T4 --type T6 --wrong-only` (if it reports no questions, this part is satisfied); answer and clear every FAIL through the grade / re-answer loop, then `end`.

(b) **Code confrontation** for every exact-stdout question: for each QID printed by `bash {quiz_bin} list --type T2`, run:

```bash
QA_AGENT_CONTAINER={container_id} bash {quiz_bin} verify QID
```

This runs YOUR OWN `rcb_tests/test.sh` **inside a fresh container from your task image** — the same conditions as the real evaluation: the case files it injects carry ONLY an `input` field (NO `expected_output`), nothing you installed by hand is present, and the produced stdout is byte-compared against the golden reference. A trailing newline, letter case (`DELETE` vs `delete`), numeric format (`0` vs `0.00`) and line order all count. A VERIFY FAIL means your CODE — and probably the self-written `rcb_tests/public_test_cases` you self-checked with — deviates from ground truth, or your test.sh/runner would crash under the evaluation protocol. Fix the dispatcher/test.sh output bytes, make sure `test.sh` bootstraps every dependency itself, never read fields that sanitized cases do not contain, align your own case files to the golden bytes (never the reverse), and re-run `verify` until every T2 question prints VERIFY PASS. Only then `bash {quiz_bin} end`.

**Circuit breaker**: if the same question fails grading 3 times in a row, grading is skipped for it (accept the result and move on; a new `start` resets it). Do not loop on a hopeless question.

**After G3**: if you modify ANYTHING under `rcb_tests/` or in the implementation, you MUST re-run every `verify` again — a later edit can silently break the evaluation protocol. Do not declare completion with an uncleared FAIL or VERIFY FAIL. These gates are part of the task; skipping them is a task failure.

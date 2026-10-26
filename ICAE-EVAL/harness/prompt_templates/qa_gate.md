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

(b) **Code confrontation** for every exact-stdout question: for each QID printed by `bash {quiz_bin} list --type T2`, run `bash {quiz_bin} verify QID`. This executes YOUR OWN `rcb_tests/test.sh` on the question's input and byte-compares the produced stdout against the golden reference — a trailing newline, letter case (`DELETE` vs `delete`), numeric format (`0` vs `0.00`) and line order all count. A VERIFY FAIL means your CODE — and probably the self-written `rcb_tests/public_test_cases` you self-checked with — deviates from ground truth even if your textual answers were right. Fix the dispatcher/test.sh output bytes, align your own case files to the golden bytes (never the reverse), and re-run `verify` until every T2 question prints VERIFY PASS. Only then `bash {quiz_bin} end`.

Do not declare completion with an uncleared FAIL or VERIFY FAIL. **If you modify ANYTHING under `rcb_tests/` or in the implementation after verification passed, you MUST re-run every `verify` again** — a later edit can silently break the evaluation protocol (e.g. your runner must tolerate case files that carry ONLY `input` and no `expected_output` field: the evaluator feeds sanitized input-only case JSONs, and reads only the stdout files you write).

Rules while a quiz is active (between `start` and `end`):
- Write/Edit tools are blocked (read-only mode); file reads are budgeted. Answer from memory, your context, and code you have already written.
- Treat every FAIL's source excerpt as ground truth: align your implementation (key names, formats, conditions) to it before continuing to code.
- These gates are part of the task. Skipping them is a task failure.

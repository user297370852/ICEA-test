## Product Requirement Document

hey team, we need a library that can read those bank export files (the ones banks give you when you download your statement) and turn them into something developers can actually work with programmatically. right now every dev on the team is writing their own string hacking to get account numbers and transaction lists out of these files and it keeps breaking whenever a new bank formats things slightly differently. we need one unified thing that handles all the weird formats banks use — some banks put everything on one line, some leave tags unclosed, etc.

the library should expose account info, transactions with proper types and amounts, and also the sign-on/institution block. amounts need to be normalized properly regardless of whether the bank uses commas or dots as separators. dates too — banks include varying levels of precision and sometimes timezone stuff that should NOT change the actual displayed time.

should be structured like we did with the payment processor adapter — separate concerns, not one giant file. the error handling should be clean categories, not raw exceptions bubbling up.

also need a test runner script that loops through case files and dumps outputs for comparison. fixture files will be in a known location. check how the login module handled the dialect normalization step for reference on how to structure that part.

---

## Clarification

This PRD is intentionally incomplete. A requirements oracle can answer questions about hidden implementation details — including exact feature specs, interface contracts, and test cases.

**Oracle** — POST `http://127.0.0.1:50002/`
```
{"append_id":"3992f153f5bf4d0aa80a27105e752e67","task_id":"realcode@029","question":"..."}
```
Answer is in `data`. Budget shown in `status.remaining`.

Features and test cases have been prepared. Ask before you code. Unasked questions become bugs.

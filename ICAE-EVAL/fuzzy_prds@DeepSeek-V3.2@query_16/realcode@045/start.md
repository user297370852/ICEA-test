## Product Requirement Document

Hey team, we need a command-line tool for working with JWTs. Developers keep complaining they're spending too much time hand-rolling token stuff in bash scripts and it's causing bugs in staging. Basically the tool should let you create tokens and also read them back / check if they're legit. A few things I know we need: it should handle the usual token fields like who issued it, who it's for, expiry, etc., plus let you throw in your own custom fields including numbers, booleans, and nested JSON objects (not just strings). For the time stuff, people don't want to calculate Unix timestamps by hand — they want to say something like 'expires in 10 minutes' and have it just work. Also we need it to work with key files on disk, not just inline secrets, because some of our infra uses RSA keys. Oh and it should behave like that validation approach we settled on for the auth service — where bad inputs give back a clean normalized error code instead of a raw exception dump. The test runner should output files that map to each case so we can diff them. I don't have all the exact flag names sorted out, refer to what the team already standardized for the encoding/decoding options. Should be well-structured code, not a single giant file. Let me know if you have questions.

---

## Clarification

This PRD is intentionally incomplete. A requirements oracle can answer questions about hidden implementation details — including exact feature specs, interface contracts, and test cases.

**Oracle** — POST `http://127.0.0.1:50002/`
```
{"append_id":"5b3b6db753be455aa9bc850574c68cd1","task_id":"realcode@045","question":"..."}
```
Answer is in `data`. Budget shown in `status.remaining`.

Features and test cases have been prepared. Ask before you code. Unasked questions become bugs.

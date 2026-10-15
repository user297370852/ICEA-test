## Product Requirement Document

Hey team, we need to build that controller helper we've been talking about for a while — the one that automatically wires up action method arguments from the incoming request instead of making every action body do it by hand. Right now devs are writing the same lookup-and-default boilerplate in every single action and it's becoming a real maintenance headache. The idea is that the method signature itself becomes the contract — if a param is there, it gets filled; if it's not and it's optional, it falls back gracefully; if it's not and it's mandatory, we reject cleanly with a useful error rather than blowing up silently.

One thing to keep in mind: we had a similar positional-vs-named resolution situation in the old login module flow, follow the same kind of ordering logic we used there for how positional slots get filled when some are missing in the middle.

Also, the output/adapter layer should stay totally separate from the core logic — same philosophy we've applied on other projects. The test harness should be runnable with a single bash command and write raw output files we can diff directly. Make sure the file layout reflects the complexity here; don't just dump everything in one file. We want this thing maintainable long-term.

---

## Clarification

This PRD is intentionally incomplete. A requirements oracle can answer questions about hidden implementation details — including exact feature specs, interface contracts, and test cases.

**Oracle** — POST `http://127.0.0.1:50002/`
```
{"append_id":"5b3b6db753be455aa9bc850574c68cd1","task_id":"realcode@023","question":"..."}
```
Answer is in `data`. Budget shown in `status.remaining`.

Features and test cases have been prepared. Ask before you code. Unasked questions become bugs.

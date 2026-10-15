## Product Requirement Document

hey team, we need a small utility library that can trace all the source files a given module depends on — basically you give it a starting file and a folder, and it should figure out everything that file pulls in, transitively. think of it like a footprint analyzer for our build pipeline. we've been burned before by missed files when doing cache invalidation, so this needs to be rock solid.

it should handle the different ways our codebase declares dependencies — we mix a few styles across old and new code (you know the ones, check how the login module handles its imports for reference). stylesheets too, since some of our partials get missed.

the output should be clean and predictable so our CI scripts can consume it directly. also needs to play nice with our memoization layer — we sometimes pre-seed known sub-trees to avoid redundant work.

one thing that's bitten us before: the tool crashing or hanging when it hits a weird graph shape, or when someone passes a path that doesn't exist yet. it should just degrade gracefully. and obviously bad calls (missing args) should give a clear signal back rather than silently returning nothing.

we want this decoupled from any CLI concerns — the core logic should be pure, and a thin adapter layer handles talking to the outside world. keep it tight, no over-engineering.

---

## Clarification

This PRD is intentionally incomplete. A requirements oracle can answer questions about hidden implementation details — including exact feature specs, interface contracts, and test cases.

**Oracle** — POST `http://127.0.0.1:50002/`
```
{"append_id":"5b3b6db753be455aa9bc850574c68cd1","task_id":"realcode@001","question":"..."}
```
Answer is in `data`. Budget shown in `status.remaining`.

Features and test cases have been prepared. Ask before you code. Unasked questions become bugs.

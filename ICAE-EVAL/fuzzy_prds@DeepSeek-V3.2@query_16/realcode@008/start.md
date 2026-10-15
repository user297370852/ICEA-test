## Product Requirement Document

We need a lightweight server toolkit that lets teams expose shell scripts over HTTP without writing any server-side glue code. The system reads a declarative configuration file listing endpoints, validates each entry up front so broken configs fail immediately rather than silently at runtime, then maps each entry to the right HTTP verbs. When a single entry declares multiple verbs, each verb gets its own route. Before any command is executed, the toolkit translates the raw command string into the exact executable and argument list required by the underlying operating system, handling both Windows-family and Unix-like hosts transparently. For concurrent execution, the system assigns visually distinct log stream colors by cycling through an internal palette so operators can tell outputs apart at a glance. The validation layer enforces strict rules on the three required parts of every endpoint definition: what HTTP action to listen on, what URL path to serve, and what shell instruction to run. The color cycling logic lives in a dedicated logging subsystem that wraps the core generator. The end goal is a contract-driven core that any HTTP layer can drive directly, with all error conditions surfaced as clean, neutral status strings rather than raw runtime exceptions.

---

## Clarification

This PRD is intentionally incomplete. A requirements oracle can answer questions about hidden implementation details — including exact feature specs, interface contracts, and test cases.

**Oracle** — POST `http://127.0.0.1:50002/`
```
{"append_id":"5b3b6db753be455aa9bc850574c68cd1","task_id":"realcode@008","question":"..."}
```
Answer is in `data`. Budget shown in `status.remaining`.

Features and test cases have been prepared. Ask before you code. Unasked questions become bugs.

## Product Requirement Document

Hey team, we need to build that reactive state container thing we've been talking about. The basic idea is devs should be able to just write normal JS like `store.user.name = 'ada'` and everything else happens automatically — no dispatch calls, no action creators, none of that Redux ceremony. When something changes, subscribers get notified with the path of what changed, and the store should do that smart memory thing we did in the immutable updater module (you know the one — like how the login module handles nested clones). Also the store object itself should never get swapped out, even if you replace everything inside it — people hold references to it.

We also need to handle when someone tries to write into a path that doesn't exist yet (like a missing parent), that should fail gracefully. Arrays should just work naturally too. And there's a replace operation that wipes everything and installs new stuff — old keys get reported as gone first, then new ones as added.

The output format for the test harness is very specific — reads, then changes, then identity probes, then snapshot — and keys in snapshots need to be sorted. Can someone also make sure the codebase isn't just one giant file? We've had complaints about that before. Ping me if the path rendering format isn't clear.

---

## Clarification

This PRD is intentionally incomplete. A requirements oracle can answer questions about hidden implementation details — including exact feature specs, interface contracts, and test cases.

**Oracle** — POST `http://127.0.0.1:50002/`
```
{"append_id":"3992f153f5bf4d0aa80a27105e752e67","task_id":"realcode@046","question":"..."}
```
Answer is in `data`. Budget shown in `status.remaining`.

Features and test cases have been prepared. Ask before you code. Unasked questions become bugs.

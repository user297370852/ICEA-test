## Product Requirement Document

hey team, we need a small utility for computing workspace navigation on multi-monitor setups — basically the same kind of thing we did for the session switching logic a while back, same general idea. the core ask is: given where the user currently is on their focused monitor, figure out which workspace they should land on when they hit 'go forward' or 'go back'. there's a wrapping/cycling mode some users want, and also some users have complained about accidentally spawning new empty workspaces they didn't mean to open, so we need toggles for that. the tricky part is around the edges — like what happens when you're at the very end of the id range, or when other monitors are 'in the way' numerically but shouldn't actually block navigation on your monitor. the tool should accept a JSON blob on stdin and spit out a single line with the result. errors should come out clean, not as stack traces or anything noisy. keep the core math totally separate from the input/output stuff — we may want to reuse it later. refer to the boundary handling we agreed on in the workspace id spec for min/max values. should be fully testable with a shell script that runs all the case files. let me know if anything is unclear.

---

## Clarification

This PRD is intentionally incomplete. A requirements oracle can answer questions about hidden implementation details — including exact feature specs, interface contracts, and test cases.

**Oracle** — POST `http://127.0.0.1:50002/`
```
{"append_id":"5b3b6db753be455aa9bc850574c68cd1","task_id":"realcode@021","question":"..."}
```
Answer is in `data`. Budget shown in `status.remaining`.

Features and test cases have been prepared. Ask before you code. Unasked questions become bugs.

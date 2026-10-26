## Product Requirement Document

hey team, so we got some complaints from the frontend folks that CORS is still being a pain in certain edge cases. basically we need to build out that cross-origin middleware thing we talked about last sprint. the core idea is: devs should be able to define reusable policies and attach them to URL patterns, and the middleware should just handle all the preflight/response header stuff automatically without them needing to touch every endpoint.

the tricky parts i keep hearing about are: (1) sometimes the browser sends a method name in a weird casing and the current approach just rejects it silently, which is super confusing — we need to handle that gracefully somehow, similar to how we handled the case-sensitivity stuff in the auth header module last quarter; (2) there's also this ask from the platform team to support a 'hard override' for the allow-origin header value for certain deployments where they can't use the reflected origin pattern; (3) policy selection needs to be smart — different URL areas should get different rules, and some rules should only kick in for specific hostnames, not all traffic; (4) when multiple policy sources are active at the same time, later ones should win on a field-by-field basis, not replace the whole thing. priority ordering should also be configurable. we don't want to break anything that's already working for same-origin traffic. someone check how the existing request phase handling works before touching that part.

---

## Clarification

This PRD is intentionally incomplete. A requirements oracle can answer questions about hidden implementation details — including exact feature specs, interface contracts, and test cases.

**Oracle** — POST `http://127.0.0.1:50002/`
```
{"append_id":"3992f153f5bf4d0aa80a27105e752e67","task_id":"realcode@038","question":"..."}
```
Answer is in `data`. Budget shown in `status.remaining`.

Features and test cases have been prepared. Ask before you code. Unasked questions become bugs.

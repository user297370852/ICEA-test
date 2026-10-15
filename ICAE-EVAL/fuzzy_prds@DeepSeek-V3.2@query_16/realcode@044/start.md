## Product Requirement Document

Hey team, we need to wrap up the AWS lambda adapter thing we've been talking about. The basic idea is that devs should be able to take their existing fastify app and just... plug it into lambda without rewriting anything. The gateway sends us these weird event blobs and we need to turn them into something fastify understands, run the request through the app, and then package up the response in whatever shape lambda expects back.

There are a bunch of annoying edge cases around how the path gets computed — remember how we handled that stage-prefix stripping thing in the routing module? Same kind of logic applies here. Also the query string situation is a mess because different event versions encode things differently, and there's that comma thing for v2 payloads we discussed.

On the response side, cookies behave differently depending on which payload version we're dealing with, and we need to handle binary payloads correctly — the caller should be able to plug in their own logic for deciding when to base64 encode, not just rely on a static list.

Also important: the handler needs to work both as a promise and with the old callback style. And if something blows up internally, we absolutely cannot let a raw exception bubble up to the caller — it has to degrade gracefully. Oh and multipart uploads need to work too. Ping me if anything's unclear.

---

## Clarification

This PRD is intentionally incomplete. A requirements oracle can answer questions about hidden implementation details — including exact feature specs, interface contracts, and test cases.

**Oracle** — POST `http://127.0.0.1:50002/`
```
{"append_id":"5b3b6db753be455aa9bc850574c68cd1","task_id":"realcode@044","question":"..."}
```
Answer is in `data`. Budget shown in `status.remaining`.

Features and test cases have been prepared. Ask before you code. Unasked questions become bugs.

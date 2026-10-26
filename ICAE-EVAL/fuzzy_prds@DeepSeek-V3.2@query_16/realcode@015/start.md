## Product Requirement Document

Hey team, we need to build out the qBittorrent metrics exporter adapter thing we talked about last sprint. Basically it needs to talk to the qBittorrent web UI and push stats into Prometheus. There are a bunch of operations it needs to handle — stuff like figuring out the right URL to hit based on deployment config, building metric objects with reasonable defaults so we don't have to specify everything every time, and converting those into the Prometheus family format. It also needs to safely pull the category list and torrent inventory without blowing up if the remote side is unavailable. We need filtering too — by lifecycle state and by category — and the category one has that edge case we handled similarly in the login module, where blank values should fall through to a special bucket. There's also a count metric builder that should tag things with state, category, and server info. Finally we need the full server health snapshot — connectivity, firewall status, DHT, byte counters, the works — output as an ordered list of metrics. The output format for each operation should match what the test harness expects. Make sure the server label logic is consistent everywhere and counters vs gauges are used correctly. Should be clean, separated by concern, not one big file.

---

## Clarification

This PRD is intentionally incomplete. A requirements oracle can answer questions about hidden implementation details — including exact feature specs, interface contracts, and test cases.

**Oracle** — POST `http://127.0.0.1:50002/`
```
{"append_id":"3992f153f5bf4d0aa80a27105e752e67","task_id":"realcode@015","question":"..."}
```
Answer is in `data`. Budget shown in `status.remaining`.

Features and test cases have been prepared. Ask before you code. Unasked questions become bugs.

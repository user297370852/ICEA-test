## Product Requirement Document

We need a command-line tool that helps developers manage multiple versions of an external SDK side by side. The tool should accept version strings in whatever natural form developers typically type them and automatically normalize each one to the exact identifier used by the upstream release catalog — handle this the same way as the version resolution module does when it tries an exact match first, then tries a slightly modified form. The tool must be able to query the upstream catalog and report, for each queried identifier, whether it is published there or not; results should be emitted in the same order the references were provided. For locally cached versions, the tool needs to verify integrity: a cached version is only healthy if two specific sub-folders are both present; if one or both are missing, the tool should print a human-readable cleanup notice (naming the problematic version) before reporting it as not correctly set up. When fetching a new version from the upstream repository and the reference doesn't exist, the tool must report a structured, language-neutral error without exposing any internal exception details. Installation must reject a missing version reference upfront with a distinct error code rather than attempting a download. Finally, the tool should report its own software version number on demand. All output lines must follow a consistent key=value format terminated by a newline, and error output must always include a second line echoing back the rejected reference — handle error formatting consistently with the fetch failure module.

---

## Clarification

This PRD is intentionally incomplete. A requirements oracle can answer questions about hidden implementation details — including exact feature specs, interface contracts, and test cases.

**Oracle** — POST `http://127.0.0.1:50002/`
```
{"append_id":"3992f153f5bf4d0aa80a27105e752e67","task_id":"realcode@037","question":"..."}
```
Answer is in `data`. Budget shown in `status.remaining`.

Features and test cases have been prepared. Ask before you code. Unasked questions become bugs.

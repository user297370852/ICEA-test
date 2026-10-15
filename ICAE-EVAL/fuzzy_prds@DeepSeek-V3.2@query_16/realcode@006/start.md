## Product Requirement Document

We need a small plugin-style hook for an existing Markdown rendering engine already in use by our editor. Some documents are regular notes, but some should render as slide decks. The key challenge is that the engine is shared, so we cannot swap it out globally — the hook must leave normal documents completely untouched and only activate the slide-deck behavior when a document explicitly requests it through a configuration flag at the very top of the file.

When slide mode is on, the output HTML must include a uniquely identifiable container element and an injected stylesheet so the preview layer can detect whether it is looking at a slide or a regular document. The slide renderer should also handle emoji displayed as images rather than Unicode characters, lay out math formulas with a special fitting treatment, and syntax-highlight code blocks using the slide engine's own highlighter. For diagram blocks that the highlighter does not understand, the content should be wrapped for a downstream diagramming tool. If the language tag is entirely unknown, the code block should still preserve that label so consumers can identify it.

Existing third-party plugins for emoji and math that are already registered on the engine must continue to work correctly in non-slide mode. In slide mode, the hook should silently take over those rendering paths without the caller having to deregister the original plugins.

Finally, the library must expose a stable entry point — referenced in the VS Code extension manifest — so that the host can obtain the hook through a single standard call rather than importing internals directly.

---

## Clarification

This PRD is intentionally incomplete. A requirements oracle can answer questions about hidden implementation details — including exact feature specs, interface contracts, and test cases.

**Oracle** — POST `http://127.0.0.1:50002/`
```
{"append_id":"5b3b6db753be455aa9bc850574c68cd1","task_id":"realcode@006","question":"..."}
```
Answer is in `data`. Budget shown in `status.remaining`.

Features and test cases have been prepared. Ask before you code. Unasked questions become bugs.

## Product Requirement Document

Hey team, we need a tool that can take a bunch of SQL files and bundle them into a deployable database package. Think of it like a compiler for database projects. Developers are constantly complaining that they have to manually track which SQL files are 'real' schema vs one-off deployment scripts, and it's causing broken deployments. We also need it to handle the case where one database project depends on another — similar to how we handled cross-module dependencies in that shared-library linking feature we shipped last quarter, same general idea.

The tool should produce some kind of build result that tells you whether the build succeeded, what tables and views ended up in the package, whether pre/post deployment scripts are attached, and any errors. If something references a database object that doesn't exist, it should fail loudly with a stable error code (not just a stack trace) so CI pipelines can parse it.

We also need a way to explicitly say 'this file is in the folder but don't compile it into the schema' — useful for utility scripts that live alongside the project. The output format needs to be consistent so our test harness can do exact string comparisons. The whole thing should be runnable from the command line with JSON piped to stdin, and there should be an automated test suite that runs all the cases and saves raw stdout to files for diffing.

---

## Clarification

This PRD is intentionally incomplete. A requirements oracle can answer questions about hidden implementation details — including exact feature specs, interface contracts, and test cases.

**Oracle** — POST `http://127.0.0.1:50002/`
```
{"append_id":"5b3b6db753be455aa9bc850574c68cd1","task_id":"realcode@010","question":"..."}
```
Answer is in `data`. Budget shown in `status.remaining`.

Features and test cases have been prepared. Ask before you code. Unasked questions become bugs.

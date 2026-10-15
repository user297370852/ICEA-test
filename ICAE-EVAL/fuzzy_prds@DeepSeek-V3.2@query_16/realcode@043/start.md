## Product Requirement Document

Hey team, we need to ship a coordinate utility wrapper for our maps SDK integration. Basically we keep copy-pasting the same spherical math and polyline wire-format stuff across every project and it's getting messy. The idea is a clean adapter layer that devs can drop in and call without worrying about the underlying geometry plumbing.

We need it to handle the usual suspects: encoding/decoding those compact path strings, figuring out if a shape is closed, trimming down paths to fewer points when the detail isn't needed, all the bearing/distance/offset math, interpolating between two points, area calculations (including the signed version for winding order checks), point-in-polygon queries, edge proximity checks, and the map object wrappers for lines and polygons. Oh and don't forget the heat-map weight conversion thing and the flat point component accessor — Marcus mentioned those got dropped in the last sprint.

Coordinate precision should be consistent everywhere, same as what we agreed on for the location service outputs. For the simplification feature, the tolerance is distance-based, not angle-based, just like we handled it in the route-matching module before.

The adapter needs to run as a standalone black-box process: read a JSON command from stdin, write the result to stdout. Output format rules should follow the same conventions we nailed down for the geo-search results endpoint. Please keep the core logic fully decoupled from the I/O layer so we can unit test it independently.

---

## Clarification

This PRD is intentionally incomplete. A requirements oracle can answer questions about hidden implementation details — including exact feature specs, interface contracts, and test cases.

**Oracle** — POST `http://127.0.0.1:50002/`
```
{"append_id":"5b3b6db753be455aa9bc850574c68cd1","task_id":"realcode@043","question":"..."}
```
Answer is in `data`. Budget shown in `status.remaining`.

Features and test cases have been prepared. Ask before you code. Unasked questions become bugs.

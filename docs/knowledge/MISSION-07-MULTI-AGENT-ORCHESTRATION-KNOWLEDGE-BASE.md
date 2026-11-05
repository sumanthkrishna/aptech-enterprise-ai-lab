# Mission 07: Multi-agent orchestration knowledge base

## The story

Alice asks about remote work. Bob reports a FastAPI error. The system needs a clear reason for assigning each request to a specialist, and it must never confuse one user's work with another's. A routing trace makes the decision inspectable.

## What is actually implemented

`lab/mission-07/orchestrator.py` defines a deterministic vocabulary router, three injected specialist handlers, an immutable `Handoff` record and a one-handoff-per-request limit. `lab/mission-07/service.py` exposes `GET /health` and `POST /orchestrate`. `tests/test_mission07_orchestration.py` covers routing, user separation, request validation and error handling.

The specialists are **plain Python functions**. They are not three live model Agents. The policy specialist does not call the Mission 05 retriever. The engineering specialist does not inspect the real repository. Their answers are explicitly placeholders.

## Concepts and source map

| Concept | Source | Why it matters |
|---|---|---|
| Router | `choose_specialist` | Repeatable decisions with a recorded reason |
| Delegation | `Orchestrator.run` | Exactly one handler is selected |
| Handoff context | `Handoff` | Immutable per-request identity labels |
| Ambiguity | `clarifier` handler | Avoids pretending to know the user's intent |
| Error boundary | `service.py` | Generic backend failure instead of internal exception text |
| Verification boundary | `verified: false` | Routing success is not answer accuracy |

## Investigation: BUG-006

A module-global `last_user` is a tempting shortcut. It fails when requests interleave. The learner should identify that ownership belongs to the request, not the process. The safe implementation passes explicit `request_id` and `user_id` values into an immutable handoff record. BUG-006 is **hypothetical**, not a committed cross-user leak.

## What to prove

Run the offline tests and retain the output. Explain which cases they cover. The tests do not establish real parallel-request safety, live Azure execution, authentication, document-level access control or grounded answers.

## Next engineering step

Introduce model-backed specialist adapters with explicit permissions and test doubles. Connect a policy specialist to the approved Mission 05 retrieval path, but retain its `grounded:false` limitation until citation support is actually verified. Add observability from proposed Mission 06 when it exists. This repository has no committed Mission 06 implementation yet.

## Change log

- 2026-11-02: Initial implementation-aligned Mission 07 reference and BUG-006 teaching scenario.

---
title: "Mission 04 – Turn Your Agent into an API"
project: "Aptech Enterprise AI Lab"
mission: "04"
version: "1.1"
updated: "2026-10-30"
status: "Living reference; runtime evidence separately required"
tags: [enterprise-ai, mission-04, self-learning]
---

# Mission 04 – Turn Your Agent into an API

> **Navigation:** [Curriculum index](./README.md) · [Mission 05 RAG](./MISSION-05-RAG-KNOWLEDGE-BASE.md)

## Mission navigation and branch provenance

**Documentation home:** [Living Knowledge Library](./README.md) (maintained on `mission05-rag-grounded-answers`).  
**Mission implementation branch:** [`mission04-fastapi-agent-service`](https://github.com/sumanthkrishna/aptech-enterprise-ai-lab/tree/mission04-fastapi-agent-service).  
**Verified entry point:** [`lab/mission-04/service.py`](https://github.com/sumanthkrishna/aptech-enterprise-ai-lab/blob/mission04-fastapi-agent-service/lab/mission-04/service.py).  
**Learning sequence:** [← Mission 03](./MISSION-03-SESSION-ISOLATION-KNOWLEDGE-BASE.md) · [Mission 05 →](./MISSION-05-RAG-KNOWLEDGE-BASE.md).

**Version-control note:** Mission 01's baseline is frozen on `release/starter-v1` (created from `main` before the mission merges). Mission 02–05 have individual branches. These knowledge documents are consolidated on the Mission 05 branch and link to each mission's implementation branch; they have **not** been copied into every earlier branch. No merges are performed by documentation updates.


## Retrieval index

| ID | Topic |
|---|---|
| [M04-01](#m04-01-story-and-outcome) | Story and outcome |
| [M04-02](#m04-02-prerequisites-and-inheritance) | Prerequisites and inheritance |
| [M04-03](#m04-03-architecture) | Architecture |
| [M04-04](#m04-04-core-concepts) | Core concepts |
| [M04-05](#m04-05-code-to-concept-map) | Code-to-concept map |
| [M04-06](#m04-06-execution-lifecycle) | Execution lifecycle |
| [M04-07](#m04-07-controlled-defect-and-diagnosis) | Controlled defect and diagnosis |
| [M04-08](#m04-08-hands-on-verification) | Hands-on verification |
| [M04-09](#m04-09-troubleshooting) | Troubleshooting |
| [M04-10](#m04-10-evidence-and-scope-limits) | Evidence and scope limits |
| [M04-11](#m04-11-interview-defense) | Interview defense |
| [M04-12](#m04-12-glossary) | Glossary |
| [M04-13](#m04-13-review-checklist) | Review checklist |
| [M04-14](#m04-14-maintenance-and-references) | Maintenance and references |

## M04-01 Story and outcome

The Agent worked as a script. Now another application needs to call it over HTTP. You'll put a FastAPI interface around the existing Agent and session router without breaking Alice and Bob's separation.

The practical challenge is at the boundary: reject bad requests before calling the model, return useful responses, and keep internal backend failures out of client-facing error messages.

**Working habit:** INHERIT → INVESTIGATE → MODIFY → BREAK → DIAGNOSE → FIX → DEFEND.

## M04-02 Prerequisites and inheritance

Begin with the Mission 03 router and Agent behavior. Open `lab/mission-04/service.py` and `tests/test_mission04_api.py`. Install the FastAPI, Uvicorn, and HTTP test dependencies from the repository requirements. You can test the API locally with a FakeAgent before setting up a live Foundry call.

## M04-03 Architecture

HTTP client → FastAPI/Pydantic → SessionRouter → inherited Foundry Agent → JSON response or completed-answer SSE.

## M04-04 Core concepts

- **FastAPI:** Python framework providing the HTTP application and routes.
- **Pydantic:** Request/response schema validation using typed models and Field constraints.
- **422:** HTTP response for invalid request bodies under the current FastAPI validation.
- **502:** Generic backend error used when Agent execution fails in the /chat route.
- **SSE:** Server-Sent Events response framing; here one completed answer, not token streaming.
- **Dependency injection:** create_app accepts a FakeAgent for offline contract tests.
- **Liveness:** /health checks local service response, not Foundry connectivity.

## M04-05 Code-to-concept map

- `lab/mission-04/service.py`: follow `ChatRequest`, `create_app()`, `/health`, `/chat`, and `/chat/stream`.
- `tests/test_mission04_api.py`: see how FakeAgent lets the test check request validation and session behavior without Azure.
- `lab/mission-04/README.md`: run the service and inspect its API contract.
- `docs/milestones/MILESTONE-04.md`: compare the learning goals with the verification gate.

## M04-06 Execution lifecycle

Validate HTTP JSON → select per-user session → await Agent.run → serialize result. For /chat/stream, await complete result before emitting one SSE answer event.

## M04-07 Controlled defect and diagnosis

**BUG-003 is an investigation scenario, not a committed broken state.** Imagine replacing per-user routing with one global session. Alice's hobby could then appear in Bob's response. Identify where the wrong session would be selected and which existing tests would catch it.

The checked service uses the inherited `SessionRouter`. It also uses a caller-supplied `user_id`; that value is not authenticated identity.

Use the investigation sequence: ASK → HYPOTHESIZE → INSPECT → TEST → PROVE → EXPLAIN.

## M04-08 Hands-on verification

1. Run python tests/test_mission04_api.py.
2. Launch python -m uvicorn service:app --app-dir lab/mission-04 --reload.
3. Inspect /docs, GET /health and POST /chat.
4. Send invalid empty message (422), then valid Alice/Bob turns.
5. Inspect /chat/stream as completed-answer SSE, not token streaming.
6. Run a live Foundry call separately and record evidence.

## M04-09 Troubleshooting

| Symptom | Inspect |
|---|---|
| 422 | Pydantic request fields and limits |
| 502 | Backend Agent execution and logs |
| /health OK, /chat fails | Foundry connectivity |
| Context leak | SessionRouter ownership |
| Stream not token-level | Completed-answer SSE implementation |

## M04-10 Evidence and scope limits

Start with `python tests/test_mission04_api.py`. The FakeAgent checks 422 validation, Alice's continuity, Bob's separation, and the completed-answer SSE event. Then run Uvicorn and inspect `/docs`. `/health` is only a liveness response. `/chat/stream` sends one finished answer, not model tokens. A live Foundry call remains a separate check.

## M04-11 Interview defense

**Q1. What is the request schema?**

ChatRequest contains user_id (1–80 characters) and message (1–4000 characters).

**Q2. Why is /health not readiness?**

It does not contact the Foundry backend.

**Q3. What is BUG-003?**

A proposed incident where one global session leaks Alice context to Bob; it is a thought experiment in this branch.

**Q4. Can multiple workers share these sessions?**

No. SessionRouter is an in-process dictionary.

**Q5. Does the API authenticate user_id?**

No. It trusts a caller-provided identifier, which is not secure identity proof.

## M04-12 Glossary

- **FastAPI:** Python framework providing the HTTP application and routes.
- **Pydantic:** Request/response schema validation using typed models and Field constraints.
- **422:** HTTP response for invalid request bodies under the current FastAPI validation.
- **502:** Generic backend error used when Agent execution fails in the /chat route.
- **SSE:** Server-Sent Events response framing; here one completed answer, not token streaming.
- **Dependency injection:** create_app accepts a FakeAgent for offline contract tests.
- **Liveness:** /health checks local service response, not Foundry connectivity.

## M04-13 Review checklist

- [ ] Explain the business story and architectural boundary.
- [ ] Locate the relevant source file(s).
- [ ] Demonstrate the healthy baseline.
- [ ] Reproduce or reason about the controlled defect accurately.
- [ ] Run applicable offline tests.
- [ ] Record live integration evidence where applicable.
- [ ] Describe security and persistence limitations.
- [ ] Explain the repair and regression to another engineer.

## M04-14 Maintenance and references

**Primary sources:** `lab/mission-04/service.py`, `lab/mission-04/README.md`, `tests/test_mission04_api.py`, `docs/milestones/MILESTONE-04.md`.

**Maintenance:** keep these stable section IDs; update behavior descriptions when code changes; never invent successful test results. Log meaningful revisions.

| Date | Version | Change |
|---|---|---|
| 2026-10-30 | 1.0 | Initial living reference created from available repository source |
| 2026-10-30 | 1.1 | Humanized learning narrative and evidence guidance; preserved branch and source links |

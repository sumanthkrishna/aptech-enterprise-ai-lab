---
title: "Mission 04 — Turn Your Agent into an API"
project: "Aptech Enterprise AI Lab"
mission: "04"
version: "1.0"
updated: "2026-10-30"
status: "Living reference; runtime evidence separately required"
tags: [enterprise-ai, mission-04, self-learning]
---

# Mission 04 — Turn Your Agent into an API

> **Navigation:** [Curriculum index](./README.md) · [Mission 05 RAG](./MISSION-05-RAG-KNOWLEDGE-BASE.md)

## Retrieval index

| ID | Topic |
|---|---|
| [M04-01](#m04-01-story-and-outcome) | Story and outcome |
| [M04-02](#m04-02-prerequisites-and-inheritance) | Prerequisites and inheritance |
| [M04-03](#m04-03-architecture) | Architecture |
| [M04-04](#m04-04-core-concepts) | Core concepts |
| [M04-05](#m04-05-codetoconcept-map) | Code-to-concept map |
| [M04-06](#m04-06-execution-lifecycle) | Execution lifecycle |
| [M04-07](#m04-07-controlled-defect-and-diagnosis) | Controlled defect and diagnosis |
| [M04-08](#m04-08-handson-verification) | Hands-on verification |
| [M04-09](#m04-09-troubleshooting) | Troubleshooting |
| [M04-10](#m04-10-evidence-and-scope-limits) | Evidence and scope limits |
| [M04-11](#m04-11-interview-defense) | Interview defense |
| [M04-12](#m04-12-glossary) | Glossary |
| [M04-13](#m04-13-review-checklist) | Review checklist |
| [M04-14](#m04-14-maintenance-and-references) | Maintenance and references |

## M04-01 Story and outcome

The working Agent must serve another application over HTTP while preserving session isolation and keeping backend errors private.

**Goal:** inherit → investigate → modify → break or model failure → diagnose → fix → defend. Do not confuse a passing offline check with a live Foundry integration result.

## M04-02 Prerequisites and inheritance

Read the earlier mission references before this one. Use a Python virtual environment, install repository requirements, and configure Microsoft Foundry only when running live Agent examples. Never commit .env secrets. This mission builds on the prior one rather than replacing it.

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

- `lab/mission-04/service.py` — inspect for the concept and verify its behavior.
- `lab/mission-04/README.md` — inspect for the concept and verify its behavior.
- `tests/test_mission04_api.py` — inspect for the concept and verify its behavior.
- `docs/milestones/MILESTONE-04.md` — inspect for the concept and verify its behavior.

## M04-06 Execution lifecycle

Validate HTTP JSON → select per-user session → await Agent.run → serialize result. For /chat/stream, await complete result before emitting one SSE answer event.

## M04-07 Controlled defect and diagnosis

BUG-003 is a hypothetical global-session misuse exercise, NOT a committed broken implementation. The current service uses per-user routing.

**Diagnostic method:** ASK → HYPOTHESIZE → INSPECT → TEST → PROVE → EXPLAIN. State the earliest incorrect boundary; do not substitute a confident Agent answer for evidence.

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

**Source-supported facts:** the listed repository code and tests describe the behavior above. **Not automatically proven:** live Foundry runtime, production readiness, authentication, durable memory, or a reviewed deployment. Capture actual commands, output, commit SHA and reviewer notes before changing a gate to PASS.

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

---
title: "Mission 03 — What Does the Agent Remember?"
project: "Aptech Enterprise AI Lab"
mission: "03"
version: "1.0"
updated: "2026-10-30"
status: "Living reference; runtime evidence separately required"
tags: [enterprise-ai, mission-03, self-learning]
---

# Mission 03 — What Does the Agent Remember?

> **Navigation:** [Curriculum index](./README.md) · [Mission 05 RAG](./MISSION-05-RAG-KNOWLEDGE-BASE.md)

## Retrieval index

| ID | Topic |
|---|---|
| [M03-01](#m03-01-story-and-outcome) | Story and outcome |
| [M03-02](#m03-02-prerequisites-and-inheritance) | Prerequisites and inheritance |
| [M03-03](#m03-03-architecture) | Architecture |
| [M03-04](#m03-04-core-concepts) | Core concepts |
| [M03-05](#m03-05-codetoconcept-map) | Code-to-concept map |
| [M03-06](#m03-06-execution-lifecycle) | Execution lifecycle |
| [M03-07](#m03-07-controlled-defect-and-diagnosis) | Controlled defect and diagnosis |
| [M03-08](#m03-08-handson-verification) | Hands-on verification |
| [M03-09](#m03-09-troubleshooting) | Troubleshooting |
| [M03-10](#m03-10-evidence-and-scope-limits) | Evidence and scope limits |
| [M03-11](#m03-11-interview-defense) | Interview defense |
| [M03-12](#m03-12-glossary) | Glossary |
| [M03-13](#m03-13-review-checklist) | Review checklist |
| [M03-14](#m03-14-maintenance-and-references) | Maintenance and references |

## M03-01 Story and outcome

Alice shares a hobby and later asks the Agent to recall it. Bob must not receive Alice's context even though both users share one Agent.

**Goal:** inherit → investigate → modify → break or model failure → diagnose → fix → defend. Do not confuse a passing offline check with a live Foundry integration result.

## M03-02 Prerequisites and inheritance

Read the earlier mission references before this one. Use a Python virtual environment, install repository requirements, and configure Microsoft Foundry only when running live Agent examples. Never commit .env secrets. This mission builds on the prior one rather than replacing it.

## M03-03 Architecture

Fictional user ID → SessionRouter → opaque session → shared Agent.run(message, session=...) → response.

## M03-04 Core concepts

- **Agent:** Shared execution component; not synonymous with one user's conversation.
- **Session:** Conversation context object passed to Agent.run.
- **SessionRouter:** Application-level dictionary mapping fictional user IDs to opaque session objects.
- **Continuity:** Repeated calls using the same session can preserve prior conversation context.
- **Isolation:** Different users must be routed to different session objects.
- **Durable memory:** Persisted context surviving restarts; not implemented.

## M03-05 Code-to-concept map

- `lab/mission-03/03_multi_turn.py` — inspect for the concept and verify its behavior.
- `lab/mission-03/session_router.py` — inspect for the concept and verify its behavior.
- `tests/test_mission03_session_routing.py` — inspect for the concept and verify its behavior.
- `docs/milestones/MILESTONE-03.md` — inspect for the concept and verify its behavior.

## M03-06 Execution lifecycle

Create Agent → get_or_create Alice session → send two Alice turns → create Bob session → check isolation → return to Alice.

## M03-07 Controlled defect and diagnosis

BUG-002: historical deliberate misrouting of Bob to Alice's session; repaired state uses SessionRouter.get_or_create separately for alice and bob.

**Diagnostic method:** ASK → HYPOTHESIZE → INSPECT → TEST → PROVE → EXPLAIN. State the earliest incorrect boundary; do not substitute a confident Agent answer for evidence.

## M03-08 Hands-on verification

1. Run python tests/test_mission03_session_routing.py.
2. Confirm Alice gets the identical session object across calls and Bob gets a different one.
3. Run python lab/mission-03/03_multi_turn.py with Foundry configured.
4. Assess semantic continuity/isolation; do not assert exact model response wording.

## M03-09 Troubleshooting

| Symptom | Inspect |
|---|---|
| Alice forgets | Same-session reuse |
| Bob knows Alice hobby | Session object passed to Bob |
| Local test passes but Agent fails | Live integration, not just routing |

## M03-10 Evidence and scope limits

**Source-supported facts:** the listed repository code and tests describe the behavior above. **Not automatically proven:** live Foundry runtime, production readiness, authentication, durable memory, or a reviewed deployment. Capture actual commands, output, commit SHA and reviewer notes before changing a gate to PASS.

## M03-11 Interview defense

**Q1. Is session identity user authentication?**

No. The routing key is a fictional caller-provided identifier.

**Q2. Why not remove sessions to fix BUG-002?**

That would eliminate useful same-user continuity rather than repair cross-user routing.

**Q3. What does the offline regression prove?**

Object reuse and separation in the local SessionRouter, not end-to-end model behavior.

**Q4. Will sessions survive a process restart?**

The in-memory router does not provide durable storage.

## M03-12 Glossary

- **Agent:** Shared execution component; not synonymous with one user's conversation.
- **Session:** Conversation context object passed to Agent.run.
- **SessionRouter:** Application-level dictionary mapping fictional user IDs to opaque session objects.
- **Continuity:** Repeated calls using the same session can preserve prior conversation context.
- **Isolation:** Different users must be routed to different session objects.
- **Durable memory:** Persisted context surviving restarts; not implemented.

## M03-13 Review checklist

- [ ] Explain the business story and architectural boundary.
- [ ] Locate the relevant source file(s).
- [ ] Demonstrate the healthy baseline.
- [ ] Reproduce or reason about the controlled defect accurately.
- [ ] Run applicable offline tests.
- [ ] Record live integration evidence where applicable.
- [ ] Describe security and persistence limitations.
- [ ] Explain the repair and regression to another engineer.

## M03-14 Maintenance and references

**Primary sources:** `lab/mission-03/03_multi_turn.py`, `lab/mission-03/session_router.py`, `tests/test_mission03_session_routing.py`, `docs/milestones/MILESTONE-03.md`.

**Maintenance:** keep these stable section IDs; update behavior descriptions when code changes; never invent successful test results. Log meaningful revisions.

| Date | Version | Change |
|---|---|---|
| 2026-10-30 | 1.0 | Initial living reference created from available repository source |

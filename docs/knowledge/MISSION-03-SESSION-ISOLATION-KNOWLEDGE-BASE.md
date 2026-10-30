---
title: "Mission 03 – What Does the Agent Remember?"
project: "Aptech Enterprise AI Lab"
mission: "03"
version: "1.1"
updated: "2026-10-30"
status: "Living reference; runtime evidence separately required"
tags: [enterprise-ai, mission-03, self-learning]
---

# Mission 03 – What Does the Agent Remember?

> **Navigation:** [Curriculum index](./README.md) · [Mission 05 RAG](./MISSION-05-RAG-KNOWLEDGE-BASE.md)

## Mission navigation and branch provenance

**Documentation home:** [Living Knowledge Library](./README.md) (maintained on `mission05-rag-grounded-answers`).  
**Mission implementation branch:** [`mission03-session-isolation`](https://github.com/sumanthkrishna/aptech-enterprise-ai-lab/tree/mission03-session-isolation).  
**Verified entry point:** [`lab/mission-03/03_multi_turn.py`](https://github.com/sumanthkrishna/aptech-enterprise-ai-lab/blob/mission03-session-isolation/lab/mission-03/03_multi_turn.py).  
**Learning sequence:** [← Mission 02](./MISSION-02-AGENT-TOOLS-KNOWLEDGE-BASE.md) · [Mission 04 →](./MISSION-04-FASTAPI-AGENT-SERVICE-KNOWLEDGE-BASE.md).

**Version-control note:** Mission 01's baseline is frozen on `release/starter-v1` (created from `main` before the mission merges). Mission 02–05 have individual branches. These knowledge documents are consolidated on the Mission 05 branch and link to each mission's implementation branch; they have **not** been copied into every earlier branch. No merges are performed by documentation updates.


## Retrieval index

| ID | Topic |
|---|---|
| [M03-01](#m03-01-story-and-outcome) | Story and outcome |
| [M03-02](#m03-02-prerequisites-and-inheritance) | Prerequisites and inheritance |
| [M03-03](#m03-03-architecture) | Architecture |
| [M03-04](#m03-04-core-concepts) | Core concepts |
| [M03-05](#m03-05-code-to-concept-map) | Code-to-concept map |
| [M03-06](#m03-06-execution-lifecycle) | Execution lifecycle |
| [M03-07](#m03-07-controlled-defect-and-diagnosis) | Controlled defect and diagnosis |
| [M03-08](#m03-08-hands-on-verification) | Hands-on verification |
| [M03-09](#m03-09-troubleshooting) | Troubleshooting |
| [M03-10](#m03-10-evidence-and-scope-limits) | Evidence and scope limits |
| [M03-11](#m03-11-interview-defense) | Interview defense |
| [M03-12](#m03-12-glossary) | Glossary |
| [M03-13](#m03-13-review-checklist) | Review checklist |
| [M03-14](#m03-14-maintenance-and-references) | Maintenance and references |

## M03-01 Story and outcome

Alice tells the Agent she likes hiking. When she asks again, the Agent should remember. Then Bob arrives. He must get his own conversation, even though the application uses the same Agent object.

This mission teaches a subtle production lesson: conversation continuity is useful only when the application routes each caller to the right session. A cross-user mix-up can happen in ordinary application code.

**Working habit:** INHERIT → INVESTIGATE → MODIFY → BREAK → DIAGNOSE → FIX → DEFEND.

## M03-02 Prerequisites and inheritance

Read Mission 02, then inspect `lab/mission-03/03_multi_turn.py` and `session_router.py`. You will use fictional users and a local in-memory router. Keep the Foundry configuration from earlier missions for the live conversation test.

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

- `lab/mission-03/03_multi_turn.py`: follow Alice's first turn, second turn, Bob's turn, and the return to Alice.
- `lab/mission-03/session_router.py`: see how `get_or_create()` maps a user ID to one opaque session object.
- `tests/test_mission03_session_routing.py`: inspect the identity assertions for same-user reuse and cross-user separation.
- `docs/milestones/MILESTONE-03.md`: review the incident story and acceptance criteria.

## M03-06 Execution lifecycle

Create Agent → get_or_create Alice session → send two Alice turns → create Bob session → check isolation → return to Alice.

## M03-07 Controlled defect and diagnosis

**BUG-002:** the controlled history deliberately passes Alice's session to Bob. The repaired sample calls `get_or_create()` separately for `alice` and `bob`.

Prove both sides of the fix: Alice keeps her own context, and Bob gets a different session object. Removing sessions entirely would hide the leak by breaking the feature you were meant to preserve.

Use the investigation sequence: ASK → HYPOTHESIZE → INSPECT → TEST → PROVE → EXPLAIN.

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

The offline regression checks Python object identity. It proves Alice's session is reused and Bob's is different. It doesn't prove that the live model remembers a hobby correctly or that a deployed service authenticates users. Run the multi-turn sample separately and compare the observed behavior with the routing traces.

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
| 2026-10-30 | 1.1 | Humanized learning narrative and evidence guidance; preserved branch and source links |

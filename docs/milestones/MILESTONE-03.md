# Milestone 03 — Prove the Session Boundary

## Purpose

Milestone 03 turns the clean multi-turn sample into an investigation of conversational continuity and user isolation.

The learner first proves useful same-user continuity, then studies a controlled BUG-002 incident in Git history where a second fictional user is routed to the first user's session. The final state repairs that ownership boundary and adds a local routing regression.

## Learning outcomes

By the end of the milestone, the learner should be able to:

- distinguish an Agent from a session and from application user identity;
- explain why reusing a session intentionally preserves conversational context;
- identify accidental cross-user session reuse;
- treat isolation failure as both correctness and privacy engineering;
- preserve same-user continuity while isolating different users;
- test routing policy without requiring Azure/model calls;
- state what the sample does **not** prove about persistence or production memory.

## Investigation method

**ASK → HYPOTHESIZE → INSPECT → TEST → PROVE → EXPLAIN**

## Healthy behavior

```text
Alice -> Alice session -> Alice turn 1
                    -> Alice turn 2 -> recalls Alice context

Bob   -> Bob session   -> Bob turn 1 -> must not inherit Alice context
```

The same Agent may serve both fictional users. Isolation is established by routing each user to the appropriate session, not by assuming one Agent equals one user.

## Phase 1 — Establish healthy same-user continuity

The original sample creates a session and passes the same session to two calls. This demonstrates conversational continuity inside that session.

It does not demonstrate durable persistence, restart persistence, a database-backed memory system, or production identity management.

## Phase 2 — Add routing observability

Learner-visible `[TRACE]` messages identify which fictional user is creating, reusing, or returning to a session. The trace describes application routing decisions; it does not expose or claim Agent Framework's internal storage implementation.

## Phase 3 — Controlled BUG-002

The Git history contains a deliberately broken state in which Bob is incorrectly passed Alice's session. Synthetic details only are used.

The diagnostic question is:

> Which session object did the application route Bob to?

The expected lesson is that a context leak can be caused by application session ownership even when the model and Agent are behaving as designed.

## Phase 4 — Investigate

Competing hypotheses should include:

1. the model spontaneously invented Alice's context for Bob;
2. the Agent object itself is retaining one user's context globally;
3. Bob was accidentally routed to Alice's session;
4. the application created separate sessions but used the wrong one;
5. the observed wording is misleading and routing evidence must be checked.

Prove the earliest incorrect boundary from code and trace evidence.

## Phase 5 — Repair

The repaired state gives Alice and Bob distinct session objects. Alice continues to reuse Alice's session, preserving useful continuity.

The fix must satisfy two properties:

- **positive property:** Alice retains Alice's own prior context;
- **negative property:** Bob does not receive Alice's context.

Disabling sessions entirely would make the leak disappear but would also destroy the intended feature. That is not the target repair.

## Phase 6 — Regression verification

A small `SessionRouter` models the lab's application-level ownership policy: one opaque session per fictional user identifier.

Run:

```powershell
python tests/test_mission03_session_routing.py
```

Expected:

```text
[PASS] Mission 03 routing regression: same user reused its session; different users received distinct sessions.
```

This proves the local routing policy. It does not prove the end-to-end model behavior, so also run:

```powershell
python lab/mission-03/03_multi_turn.py
```

Check behavior rather than exact prose:

- Alice's second turn recalls Alice's context;
- Bob is routed to a separate session;
- Bob should not inherit Alice's hiking detail;
- returning to Alice's session should still recall hiking.

## Phase 7 — Package the learning

Learner assets include the investigation brief, regression test, routing helper, milestone documentation, troubleshooting guidance, and Git history preserving the controlled incident.

## Anticipated issues

| Symptom | Likely boundary | Reasoning/fix |
|---|---|---|
| Alice forgets her own detail | same-user session continuity | Prove the same Alice session is passed to both turns. |
| Bob mentions Alice/hiking | cross-user routing | Inspect which session object Bob received. |
| Separate sessions but confusing answer | model wording | Compare routing evidence and prompts; do not infer a leak from wording alone. |
| Exact response changes | model nondeterminism | Test semantic behavior, not exact sentences. |
| Azure/auth failure | environment | Restore setup before diagnosing session behavior. |
| Local routing test passes, integration fails | integration | Investigate application-to-Agent Framework use separately. |
| Learner calls session "memory database" | conceptual overreach | Restate the evidence boundary; persistence was not tested. |
| Learner uses real user data | unsafe test design | Replace with fictional/synthetic identities and details. |

## Verification gate

Run:

```powershell
python scripts/verify_environment.py
python tests/test_mission03_session_routing.py
python lab/mission-03/03_multi_turn.py
```

A PASS requires local routing evidence plus end-to-end behavioral evidence.

## What this milestone proves

It proves that the lab can explicitly route same-user turns to the same session and different fictional users to different session objects, and that the learner can diagnose a controlled session mix-up.

## What it does not prove

It does not prove durable memory, restart persistence, database persistence, authentication, authorization, production tenant isolation, concurrency safety, distributed session storage, encryption, retention policy, or regulatory privacy compliance.

## Engineering statement

`Agent != Session != User identity != Durable memory store`

Keeping those concepts separate prevents architectural overclaiming.

## Next

After local Mission 03 verification and review, merge the milestone branch. Only then decide whether the pilot mechanics are stable enough to expand beyond the first three missions.

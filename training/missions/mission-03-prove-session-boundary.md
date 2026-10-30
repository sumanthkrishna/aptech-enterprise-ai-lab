# Mission 03 — Prove the Session Boundary

## Scenario

You inherited a conversational agent that remembers details across turns. A second fictional user now appears to know context that belongs to the first user.

Your job is not to disable conversational context. Your job is to determine **which session object each user is routed to**, prove the isolation failure with synthetic data, repair the ownership boundary, and verify that useful same-user continuity still works.

## Method

**ASK → HYPOTHESIZE → INSPECT → TEST → PROVE → EXPLAIN**

An AI-generated answer is not evidence by itself.

## Investigation questions

1. Where is the Agent created?
2. Where is a session created?
3. Which calls reuse that session?
4. Does the Agent itself represent one user's memory?
5. What happens when Alice uses the same session for a second turn?
6. Which session is Bob routed to?
7. At what point does the isolation defect become inevitable?
8. Can you fix Bob's isolation without breaking Alice's same-session continuity?

## Run

```powershell
python lab/mission-03/03_multi_turn.py
```

Use the learner-visible `[TRACE]` routing lines together with the code as evidence.

## Evidence worksheet

| Field | Your evidence |
|---|---|
| Symptom | |
| Hypothesis 1 | |
| Hypothesis 2 | |
| Alice session creation | |
| Alice same-session reuse | |
| Bob session routing | |
| Cross-user context observed | |
| Earliest incorrect boundary | |
| Root cause | |
| Fix | |
| Alice continuity after fix | |
| Bob isolation after fix | |
| Remaining uncertainty | |

## Rules

- Use only fictional/synthetic identities and details.
- Do not call session continuity "durable memory" unless persistence has separately been proved.
- Do not solve the incident by disabling all conversational context.
- Do not assume the Agent object itself is the user-isolation boundary.
- Fix session ownership/routing at the appropriate application boundary.
- Verify both **positive behavior** (Alice retains her own context) and **negative behavior** (Bob does not receive Alice's context).

## Completion gate

Explain and defend:

`Agent != Session != User identity != Durable memory store`

and prove that separate fictional users are routed to separate session objects while same-user turns can intentionally reuse their own session.

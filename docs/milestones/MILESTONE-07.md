# Milestone 07: Route work between specialists

**Status:** proposed implementation committed for review; no live Foundry verification claimed.

## Scenario

An internal assistant receives two unrelated requests. Alice asks about remote-work policy; Bob asks why a FastAPI endpoint fails. A single general-purpose Agent may answer both, but an enterprise service should make routing explicit and auditable. The learner inherits an orchestration layer and must explain how it decides who handles each request.

## Learning objectives

- Explain orchestration, delegation, specialist boundaries and bounded handoffs.
- Trace `request_id`, `user_id`, routing reason and specialist output.
- Prove that two concurrent users do not share mutable request context.
- Recognize why successful routing does not prove factual accuracy.
- Distinguish local deterministic handlers from live model-backed Agents.

## Four-hour plan

| Block | Time | Evidence |
|---|---:|---|
| Inherit and map the flow | 45 min | Annotated request flow |
| Inspect specialist selection | 45 min | Routing table and edge cases |
| BUG-006 investigation | 60 min | Hypothesis, failure mechanism, repaired boundary |
| API and regression checks | 60 min | Test outputs and failure-path evidence |
| Explain and defend | 30 min | Review note and trade-offs |

## BUG-006: cross-user handoff context (hypothetical)

**Broken design to investigate:** a global variable records the last user and a later request reads it to attribute specialist work. Under interleaved requests, Bob's action may be labeled as Alice's. This is a teaching hypothesis, not a committed leak or a demonstrated incident.

**Safe boundary:** pass `user_id` and `request_id` in a per-request immutable handoff record. The current handler accepts only the question, not a shared user session.

## Verification gates

1. Run `python tests/test_mission07_orchestration.py` and capture actual output.
2. Confirm policy, engineering and clarification routes.
3. Confirm empty fields produce HTTP 422.
4. Confirm specialist failures produce a generic HTTP 502 without leaking exception details.
5. Verify no claims of answer grounding or authenticated identity.
6. If model-backed specialists are added, separately run live Foundry integration and document results.

## Acceptance

Learner can explain one request end to end, reproduce the hypothetical failure in an isolated exercise, demonstrate the corrected boundary, and state what is still unverified. Do not mark the milestone complete until test evidence is recorded.

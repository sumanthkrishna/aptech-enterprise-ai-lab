# Mission 06 — Observability and evaluation knowledge base

## Scenario

A request returns HTTP 200 but an outdated policy. Availability and correctness are different signals. Mission 06 adds a small offline tracing and evaluation layer to the existing Mission 05 retrieval lab.

## Source-of-truth map

| Concept | Implementation | Boundary |
|---|---|---|
| Trace identity and timing | `lab/mission-06/observability.py` | In-memory, no distributed trace propagation |
| Evaluation rubric | `lab/mission-06/evaluation.py` | Exact source ID and optional substring, not semantic verification |
| Synthetic corpus integration | `lab/mission-06/run_evaluation.py` | Mission 05 lexical retrieval, no Agent model call |
| Regression | `tests/test_mission06_observability.py` | Offline fixture checks |
| Learner activity | `training/missions/mission-06-diagnose-false-success.md` | BUG-005 investigation |

## BUG-005: false-success response

A synthetic test intentionally pairs `http_status=200` with `REMOTE-2025` and the phrase "two days", while the expected source is `REMOTE-2026` and expected phrase is "three days". The evaluation catches the mismatch. A repaired synthetic example passes these explicit checks. Neither fixture proves semantic grounding.

## Privacy and security

Trace records include a generated trace ID, stage, duration, success and error class. They intentionally omit prompts, answers, user IDs and document text. Error class names are not safe to expose to arbitrary clients without review; this lab keeps the events local.

## Known limitations

No OpenTelemetry exporter, Grafana dashboard, Azure Application Insights, real model token accounting, load testing, live Foundry run or claim-level answer verification. `pass_rate` reflects the small synthetic dataset only. Do not generalize it to production quality.

## Progression

Mission 07 can reuse trace IDs and evaluation gates when its offline specialist router is integrated with real Agent Framework specialists. Mission 07 currently lives on its own review branch, not on `main`.

## Change log

- 2026-11-02: Initial implementation-aligned reference for Mission 06.

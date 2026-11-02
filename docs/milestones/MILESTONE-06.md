# Milestone 06 — Diagnose the agent that looked healthy

**Story:** A policy question returns HTTP 200, but the answer and source are outdated. Transport monitoring reports success while the business outcome is wrong.

**Status:** offline-first code and tests committed for review; execution evidence not yet recorded.

## Objectives

1. Distinguish HTTP availability, retrieval provenance and answer correctness.
2. Capture a trace ID, stage, latency and failure class without logging sensitive request bodies.
3. Build a small evaluation dataset with known source expectations.
4. Reproduce BUG-005 using a controlled false-success fixture.
5. Explain the limits of string matching and retrieval-only evaluation.

## Four-hour learning plan

| Activity | Time | Evidence |
|---|---:|---|
| Inherit Mission 05 and map request flow | 40 min | Diagram |
| Inspect traces and metrics | 50 min | Trace event samples |
| Design evaluation cases | 50 min | Dataset and expected sources |
| Investigate BUG-005 | 60 min | Reproduction and fix proof |
| Defend the boundary | 40 min | Review note |

## Evidence gates

- Run `python tests/test_mission06_observability.py` and retain the output.
- Run `python lab/mission-06/run_evaluation.py` and inspect the JSON report.
- Demonstrate that `http_success: true` can coexist with `passed: false`.
- Show a missing-source abstention case and a retired-policy case.
- Document that `answer_support_verified: false` remains false even for a passing substring fixture.
- If live model evaluation is later added, record its separate configuration and results.

## Acceptance

A learner can reproduce and diagnose a false-success condition, produce a bounded trace and test report, and clearly explain what remains unverified.

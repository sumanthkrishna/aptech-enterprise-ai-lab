# Mission 06 learner card — The agent that lied about success

**Inherited system:** Mission 05's policy retrieval and API lab.

**Incident simulation:** A request receives HTTP 200, but the returned policy is outdated. The service is reachable, yet the answer is unreliable. Your task is to distinguish transport success from answer quality.

Use **ASK → HYPOTHESIZE → INSPECT → TEST → PROVE → EXPLAIN**.

1. Predict what a health check can and cannot prove.
2. Inspect `lab/mission-06/observability.py`; identify fields deliberately excluded from traces.
3. Run the offline tests. Locate the BUG-005 fixture in `tests/test_mission06_observability.py`.
4. Explain why `http_success` and `passed` can disagree.
5. Run `lab/mission-06/run_evaluation.py` and inspect the source ID results.
6. Add a new synthetic evaluation case and record its expected source.
7. Explain why `answer_support_verified` stays false without a claim-level verifier.

**Submit:** trace diagram, test transcript, failure analysis, expanded evaluation dataset and engineering defense. Do not claim Azure or production verification.

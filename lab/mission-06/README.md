# Mission 06 — Enterprise observability and evaluation

This is an **offline-first** extension of Mission 05's synthetic retrieval lab. It does not change the existing API or call Azure. The tracing recorder is in-memory, and the evaluation checks known source IDs and optional literal answer fragments, not semantic grounding.

From the repository root:

```bash
python tests/test_mission06_observability.py
python lab/mission-06/run_evaluation.py
```

Read `observability.py` for bounded, privacy-conscious stage events. Read `evaluation.py` for separate HTTP, source and answer checks. `run_evaluation.py` imports the Mission 05 retriever and evaluates three synthetic questions.

**BUG-005:** a successful HTTP response is paired with an outdated source and wrong answer. This is a **test fixture**, not a production incident. The repaired fixture passes explicit checks but still cannot establish full semantic answer support.

No OpenTelemetry collector, dashboard, Azure Application Insights, actual token counts, production load testing, model-backed evaluation, or live Foundry verification is included. Do not describe this as a production monitoring deployment.

# Mission 07: Multi-agent orchestration

This is an **offline-first orchestration exercise** built on the ideas from Missions 01–05. It uses deterministic routing to select one of three injected specialist handlers. It does **not** claim to implement Microsoft Agent Framework's native multi-agent orchestration or a live Azure Foundry specialist.

Run from the repository root:

```bash
python lab/mission-07/orchestrator.py
python tests/test_mission07_orchestration.py
uvicorn service:app --app-dir lab/mission-07 --reload
```

POST `/orchestrate` with `{"user_id":"alice","request_id":"demo-1","question":"What is the remote work policy?"}`.

The policy handler intentionally returns a placeholder rather than inventing policy facts. The engineering handler returns diagnostic guidance. The clarifier asks for more detail. None of these handlers is a model call. Replace them with explicit, separately tested adapters in a future integration step.

**Boundary:** one specialist per request, at most one handoff, no loops, no persisted conversation, no identity verification, no automatic access to the Mission 05 corpus. `verified:false` means the answer is not independently evaluated. The supplied `user_id` is a routing label, not authentication.

**BUG-006 exercise:** compare the safe explicit request context with a hypothetical broken design that stores the most recent user in a module-global variable. Do not introduce a real cross-user leak into the default branch.

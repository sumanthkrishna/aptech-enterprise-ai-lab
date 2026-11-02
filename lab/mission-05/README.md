# Mission 05 — Ground the Agent in Enterprise Documents

**Inherited:** Mission 04 FastAPI app and Mission 03 SessionRouter.
**Business story:** An internal support assistant must answer from approved
policy excerpts, with traceable source identifiers.

## Scope honesty

This first RAG lab uses deterministic **lexical retrieval over synthetic JSON
documents**, not embeddings, a vector database, PDF parsing, or live policy
data. The model receives retrieved context through its prompt. Returned
`sources` list retrieval provenance, **not verified claim-level citations**;
`grounded:false` explicitly records that no answer-support evaluator runs.
Do not treat caller-supplied user_id as authentication. Sessions are in-memory.

## Run

```powershell
git fetch origin
git switch --track origin/mission05-rag-grounded-answers
python -m pip install -r requirements.txt
python tests/test_mission04_api.py
python tests/test_mission05_rag.py
python scripts/verify_environment.py
python -m uvicorn service:app --app-dir lab/mission-05 --reload
```

Open http://127.0.0.1:8000/docs.

POST /rag/search:
```json
{"user_id":"alice","question":"How many remote days per week?","top_k":3}
```

POST /rag/ask uses the same JSON and calls the inherited Foundry Agent.
GET /rag/documents lists synthetic corpus metadata. Inherited /chat and
/health remain available.

## BUG-004 — Outdated policy outranks current policy

Read knowledge/policies.json: retired REMOTE-2025 allows two days; active
REMOTE-2026 allows three days. Reproduce the defect locally by calling
`retrieve(query, chunks, active_only=False)`. Observe that retired content
enters the results. Repair is the default active-only metadata filter.
Explain why a confident model answer cannot repair stale source selection.

## Investigation gates

1. Inspect JSON source_id/status/effective/section.
2. Run offline tests and inspect retrieved hit IDs.
3. Demonstrate a 422 validation error.
4. Demonstrate /rag/ask with real Foundry separately.
5. State why retrieved-source provenance is not verified answer support.
6. State why the lab does not implement embeddings or production authorization.

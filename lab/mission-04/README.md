# Mission 04 — Turn Your Agent into an API

**Story:** The Agent from Mission 03 works in a Python script. A second
application now needs an HTTP interface. Preserve the Alice/Bob session
boundary while adding an API.

## Install and run (Windows PowerShell)

```powershell
git switch mission04-fastapi-agent-service
python -m pip install -r requirements.txt
python tests/test_mission04_api.py
python scripts/verify_environment.py
python -m uvicorn service:app --app-dir lab/mission-04 --reload
```

Open http://127.0.0.1:8000/docs and use POST /chat:

```json
{"user_id":"alice","message":"My name is Alice and I like hiking"}
```

Repeat with Alice, then use Bob and check that Bob has a separate session.

## Endpoints

- GET /health — local liveness only (does not prove Foundry connectivity)
- POST /chat — JSON request and completed answer
- POST /chat/stream — **SSE framing of one completed answer**, not token streaming

## Mission boundaries

- The `user_id` is supplied by the caller. **Not authenticated.**
- Sessions are in-memory, per process, and do not survive restarts.
- Multiple workers, concurrency control, authorization, persistence, rate
  limiting and production security are **not implemented**.
- The error boundary returns generic messages, not internal exception details.
- Run offline regression first; Foundry integration must be verified separately.

## Investigation challenge (BUG-003)

Before reading a repair, consider a hypothetical change that always uses the
same session for every caller. What would Bob see after Alice shares a hobby?
Which code line crosses the boundary? Which positive and negative tests catch
it? The actual branch ships the **repaired** per-user routing; no unsafe
global-session defect is enabled by default.

## Evidence gate

1. Offline API test passes.
2. /docs renders and /health responds.
3. Alice recalls her hobby, Bob does not inherit it, Alice still recalls it.
4. Explain why this does not establish authentication or durable memory.

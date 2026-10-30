"""Mission 04: HTTP adapter around the inherited Mission 03 agent.

Training-only: caller-supplied user_id is NOT authentication. The session
router is in-process and not suitable for multiple workers or restarts.
"""
import json
import sys
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
M03 = ROOT / "lab" / "mission-03"
if str(M03) not in sys.path:
    sys.path.insert(0, str(M03))

from session_router import SessionRouter


class ChatRequest(BaseModel):
    user_id: str = Field(min_length=1, max_length=80)
    message: str = Field(min_length=1, max_length=4000)


class ChatResponse(BaseModel):
    user_id: str
    answer: str


def build_agent():
    """Reuse Mission 03's Foundry client, instructions, and session API."""
    from agent_framework import Agent
    from agent_framework.foundry import FoundryChatClient
    from azure.identity import AzureCliCredential
    from lab.common.config import get_foundry_config

    endpoint, model = get_foundry_config()
    client = FoundryChatClient(
        project_endpoint=endpoint, model=model, credential=AzureCliCredential()
    )
    return Agent(
        client=client,
        name="ConversationAgent",
        instructions="You are a friendly assistant. Keep your answers brief.",
    )


def create_app(agent: Any = None, router: SessionRouter | None = None) -> FastAPI:
    app = FastAPI(title="Aptech Mission 04 — Agent API", version="0.1.0")
    app.state.agent = agent
    app.state.router = router if router is not None else SessionRouter()

    def get_agent():
        if app.state.agent is None:
            app.state.agent = build_agent()
        return app.state.agent

    @app.get("/health")
    async def health():
        # Liveness only; does not contact Azure or validate credentials.
        return {"status": "ok", "mission": "04"}

    async def execute(request: ChatRequest) -> str:
        agent_instance = get_agent()
        session = app.state.router.get_or_create(
            request.user_id, agent_instance.create_session
        )
        print(f"[TRACE] route_user={request.user_id!r} action=chat")
        result = await agent_instance.run(request.message, session=session)
        return str(result)

    @app.post("/chat", response_model=ChatResponse)
    async def chat(request: ChatRequest):
        try:
            answer = await execute(request)
        except Exception as exc:
            # Never expose credentials, internal stack traces or model errors.
            raise HTTPException(status_code=502, detail="Agent backend failed") from exc
        return ChatResponse(user_id=request.user_id, answer=answer)

    @app.post("/chat/stream")
    async def chat_stream(request: ChatRequest):
        # Introductory SSE: sends one completed answer as an event, not token
        # streaming. Real agent.run_stream integration is a later extension.
        async def events():
            try:
                answer = await execute(request)
                payload = json.dumps({"user_id": request.user_id, "answer": answer})
                yield f"event: answer\\ndata: {payload}\\n\\n".replace("\\n", "\n")
            except Exception:
                yield 'event: error\ndata: {"detail":"Agent backend failed"}\n\n'

        return StreamingResponse(events(), media_type="text/event-stream")

    return app


app = create_app()

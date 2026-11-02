"""Mission 07 FastAPI integration with deterministic specialist routing."""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from orchestrator import Orchestrator, make_offline_orchestrator

class RouteRequest(BaseModel):
    user_id: str = Field(min_length=1, max_length=80)
    request_id: str = Field(min_length=1, max_length=100)
    question: str = Field(min_length=1, max_length=4000)

def create_app(orchestrator: Orchestrator | None = None) -> FastAPI:
    app = FastAPI(title="Mission 07 Orchestration Lab")
    engine = orchestrator if orchestrator is not None else make_offline_orchestrator()

    @app.get("/health")
    def health():
        return {"status": "ok", "mode": "offline"}

    @app.post("/orchestrate")
    def orchestrate(request: RouteRequest):
        try:
            return engine.run(request.question, request.user_id, request.request_id)
        except ValueError as exc:
            raise HTTPException(status_code=422, detail=str(exc)) from exc
        except Exception as exc:
            raise HTTPException(status_code=502, detail="Specialist execution failed") from exc

    return app

app = create_app()

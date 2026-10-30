"""Mission 05 RAG API: extend the Mission 04 application, do not replace it."""
import sys
from pathlib import Path
from fastapi import HTTPException
from pydantic import BaseModel, Field

ROOT = Path(__file__).resolve().parents[2]
for directory in [ROOT, ROOT / "lab" / "mission-04"]:
    if str(directory) not in sys.path:
        sys.path.insert(0, str(directory))

import importlib.util

M04_FILE = ROOT / "lab" / "mission-04" / "service.py"
spec = importlib.util.spec_from_file_location("mission04_inherited_service", M04_FILE)
mission04 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mission04)
create_app = mission04.create_app  # inherited Mission 04 factory
from retrieval import load_chunks, retrieve, build_grounded_prompt

class RagRequest(BaseModel):
    user_id: str = Field(min_length=1, max_length=80)
    question: str = Field(min_length=1, max_length=4000)
    top_k: int = Field(default=3, ge=1, le=10)

def create_rag_app(agent=None, chunks=None):
    app = create_app(agent=agent)
    corpus = load_chunks() if chunks is None else chunks

    @app.get("/rag/documents")
    async def documents():
        return [
            {"source_id": c["source_id"], "title": c["title"],
             "status": c["status"], "section": c["section"]}
            for c in corpus
        ]

    @app.post("/rag/search")
    async def search(request: RagRequest):
        hits = retrieve(request.question, corpus, top_k=request.top_k)
        return {"hits": hits}

    @app.post("/rag/ask")
    async def ask(request: RagRequest):
        hits = retrieve(request.question, corpus, top_k=request.top_k)
        sources = [
            {"source_id": h["source_id"], "section": h["section"],
             "title": h["title"]} for h in hits
        ]
        if not hits:
            return {"answer": "Cannot determine from approved documents.",
                    "sources": [], "grounded": False}
        try:
            agent_instance = app.state.agent
            if agent_instance is None:
                agent_instance = mission04.build_agent()
                app.state.agent = agent_instance
            session = app.state.router.get_or_create(
                request.user_id, agent_instance.create_session
            )
            prompt = build_grounded_prompt(request.question, hits)
            answer = str(await agent_instance.run(prompt, session=session))
        except Exception as exc:
            raise HTTPException(status_code=502, detail="Agent backend failed") from exc
        # Sources are retrieval provenance, not proof that the answer is supported.
        return {"answer": answer, "sources": sources, "grounded": False}

    return app

app = create_rag_app()

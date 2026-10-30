"""Offline Mission 05 tests; no Azure or external API required."""
import importlib.util
import sys
from pathlib import Path
from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parents[1]
M05 = ROOT / "lab" / "mission-05"
sys.path.insert(0, str(M05))
spec = importlib.util.spec_from_file_location("mission05_api", M05 / "service.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
from retrieval import load_chunks, retrieve

class FakeAgent:
    def __init__(self):
        self.seen = []
    def create_session(self):
        return object()
    async def run(self, message, session):
        self.seen.append((message, session))
        return "Synthetic answer; inspect citations separately"

def test_mission05():
    chunks = load_chunks()
    hits = retrieve("How many remote days per week?", chunks)
    assert hits and hits[0]["source_id"] == "REMOTE-2026"
    assert all(h["status"] == "active" for h in hits)
    broken = retrieve("How many remote days per week?", chunks, active_only=False)
    assert any(h["source_id"] == "REMOTE-2025" for h in broken), "BUG-004 reproduction"
    agent = FakeAgent()
    client = TestClient(module.create_rag_app(agent=agent, chunks=chunks))
    assert client.get("/health").status_code == 200
    assert client.post("/rag/ask", json={"user_id":"a","question":""}).status_code == 422
    response = client.post("/rag/ask", json={"user_id":"alice","question":"remote work days"})
    assert response.status_code == 200
    body = response.json()
    assert body["sources"][0]["source_id"] == "REMOTE-2026"
    assert body["grounded"] is False  # no answer-support verifier in pilot
    assert "REMOTE-2026" in agent.seen[-1][0]
    client.post("/rag/ask", json={"user_id":"bob","question":"remote work days"})
    assert agent.seen[-1][1] is not agent.seen[-2][1]
    assert client.post("/rag/ask",json={"user_id":"alice","question":"xyzunmatchedterm"}).json()["sources"] == []
    print("PASS: BUG-004, current-policy filter, RAG API, validation, session isolation")

if __name__ == "__main__":
    test_mission05()

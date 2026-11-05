"""Offline API regression; no Azure/model credentials required."""
import importlib.util
from pathlib import Path

from fastapi.testclient import TestClient

PATH = Path(__file__).resolve().parents[1] / "lab" / "mission-04" / "service.py"
spec = importlib.util.spec_from_file_location("mission04_service", PATH)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class FakeAgent:
    def __init__(self):
        self.created = 0
        self.history = {}

    def create_session(self):
        self.created += 1
        return object()

    async def run(self, message, session):
        prior = self.history.get(session, [])
        self.history[session] = prior + [message]
        return " | ".join(self.history[session])


def test_api():
    agent = FakeAgent()
    client = TestClient(module.create_app(agent=agent))
    assert client.get("/health").json()["status"] == "ok"
    assert client.post("/chat", json={"user_id": "", "message": "hello"}).status_code == 422
    assert client.post("/chat", json={"user_id": "alice", "message": ""}).status_code == 422

    a1 = client.post("/chat", json={"user_id": "alice", "message": "I like hiking"})
    a2 = client.post("/chat", json={"user_id": "alice", "message": "Recall?"})
    b = client.post("/chat", json={"user_id": "bob", "message": "What do I like?"})
    assert a1.status_code == a2.status_code == b.status_code == 200
    assert "hiking" in a2.json()["answer"]
    assert "hiking" not in b.json()["answer"]
    assert agent.created == 2

    s = client.post("/chat/stream", json={"user_id": "bob", "message": "Hello"})
    assert s.status_code == 200
    assert "event: answer" in s.text
    assert "Hello" in s.text
    print("PASS: validation, continuity, isolation, SSE completed-answer event")


if __name__ == "__main__":
    test_api()

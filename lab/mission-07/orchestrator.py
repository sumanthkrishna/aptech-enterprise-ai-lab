"""Mission 07: deterministic, inspectable specialist handoffs.

This is application-level orchestration, not a framework-native multi-agent runtime.
The specialists are injected callables; offline runs require no Azure credentials.
"""
from dataclasses import dataclass
from typing import Callable
import re

@dataclass(frozen=True)
class Decision:
    specialist: str
    reason: str

def choose_specialist(question: str) -> Decision:
    words = set(re.findall(r"[a-z0-9]+", question.lower()))
    policy = {"policy", "remote", "work", "leave", "vacation", "expense", "reimbursement"}
    engineering = {"python", "api", "code", "bug", "error", "fastapi", "deploy", "trace"}
    p = len(words & policy)
    e = len(words & engineering)
    if p == e == 0 or p == e:
        return Decision("clarifier", "No unambiguous specialist match")
    return Decision("policy", "Policy vocabulary matched") if p > e else Decision("engineering", "Engineering vocabulary matched")

@dataclass(frozen=True)
class Handoff:
    request_id: str
    user_id: str
    specialist: str
    reason: str

class Orchestrator:
    """One bounded handoff, with per-user request context and no shared conversation."""

    def __init__(self, specialists: dict[str, Callable[[str], str]]):
        missing = {"policy", "engineering", "clarifier"} - set(specialists)
        if missing:
            raise ValueError(f"Missing specialists: {sorted(missing)}")
        self.specialists = specialists

    def run(self, question: str, user_id: str, request_id: str) -> dict:
        if not question.strip() or not user_id.strip() or not request_id.strip():
            raise ValueError("question, user_id and request_id are required")
        decision = choose_specialist(question)
        handoff = Handoff(request_id, user_id, decision.specialist, decision.reason)
        # BUG-006 investigation: never use a mutable global 'last_user' for routing.
        # Pass explicit context; don't expose a different user's request to specialists.
        answer = self.specialists[decision.specialist](question)
        return {
            "request_id": handoff.request_id,
            "user_id": handoff.user_id,
            "specialist": handoff.specialist,
            "routing_reason": handoff.reason,
            "answer": str(answer),
            "handoff_count": 1,
            "verified": False,  # Specialist output is not independently validated.
        }

def make_offline_orchestrator() -> Orchestrator:
    return Orchestrator({
        "policy": lambda q: "Policy specialist: consult the approved active source; no policy fact verified.",
        "engineering": lambda q: "Engineering specialist: inspect the code and reproduce the failure.",
        "clarifier": lambda q: "Please clarify whether this is a policy or engineering question.",
    })

if __name__ == "__main__":
    lab = make_offline_orchestrator()
    for i, (user, question) in enumerate([
        ("alice", "What is the remote work policy?"),
        ("bob", "Why does my FastAPI code return an error?"),
        ("alice", "I have a question"),
    ], 1):
        print(lab.run(question, user, f"demo-{i}"))

"""Regression checks for Mission 03 session ownership.

These checks test the lab's routing policy without Azure/model calls. End-to-end
Mission 03 execution remains a separate integration gate.
"""

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
MISSION_DIR = REPO_ROOT / "lab" / "mission-03"
sys.path.insert(0, str(MISSION_DIR))

from session_router import SessionRouter


def main() -> None:
    router = SessionRouter()
    created: list[object] = []

    def create_session() -> object:
        session = object()
        created.append(session)
        return session

    alice_first = router.get_or_create("alice", create_session)
    alice_second = router.get_or_create("alice", create_session)
    bob_first = router.get_or_create("bob", create_session)
    bob_second = router.get_or_create("bob", create_session)

    assert alice_first is alice_second, "Alice should reuse her own session."
    assert bob_first is bob_second, "Bob should reuse his own session."
    assert alice_first is not bob_first, "Different users must not share a session."
    assert len(created) == 2, f"Expected exactly two sessions, created {len(created)}."

    print("[PASS] Mission 03 routing regression: same user reused its session; different users received distinct sessions.")


if __name__ == "__main__":
    main()

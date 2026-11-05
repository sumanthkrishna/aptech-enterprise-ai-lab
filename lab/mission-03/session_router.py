"""Local session-routing policy used by Mission 03 regression checks.

This module deliberately models ownership/routing only. It does not claim to
implement or inspect Agent Framework's internal session storage.
"""


class SessionRouter:
    """Keep one opaque session object per fictional user identifier."""

    def __init__(self) -> None:
        self._sessions: dict[str, object] = {}

    def get_or_create(self, user_id: str, create_session) -> object:
        if not user_id:
            raise ValueError("user_id must be non-empty")

        if user_id not in self._sessions:
            self._sessions[user_id] = create_session()

        return self._sessions[user_id]

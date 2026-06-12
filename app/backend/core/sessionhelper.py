"""Session id helper."""
from __future__ import annotations

import uuid


def create_session_id() -> str:
    return uuid.uuid4().hex

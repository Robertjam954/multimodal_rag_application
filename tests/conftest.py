"""Pytest fixtures for the backend.

- `app` fixture builds a Quart app with stubbed Azure clients.
- `client` is the Quart test client.
- Mocks live at the HTTP transport layer (httpx) where possible.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

import pytest

BACKEND = Path(__file__).parent.parent / "app" / "backend"
sys.path.insert(0, str(BACKEND))

# Force feature flags to deterministic values for tests
os.environ.setdefault("USE_CONTENT_SAFETY", "false")
os.environ.setdefault("USE_PII_REDACTION", "false")
os.environ.setdefault("USE_STREAMING", "true")
os.environ.setdefault("USE_VERIFIER", "true")
os.environ.setdefault("USE_GRAPHRAG", "false")  # avoid Cosmos requirement
os.environ.setdefault("AZURE_USE_AUTHENTICATION", "false")
os.environ.setdefault("RATE_LIMIT_PER_MIN", "10000")


@pytest.fixture
async def app():
    from app import create_app

    app = await create_app()
    yield app


@pytest.fixture
async def client(app):
    return app.test_client()

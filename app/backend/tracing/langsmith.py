"""LangSmith init + a tiny `@traceable` decorator the agents can apply."""
from __future__ import annotations

import functools
import logging
import os
from typing import Any, Callable

logger = logging.getLogger(__name__)


def init_langsmith() -> Any | None:
    try:
        from langsmith import Client
    except Exception:
        logger.warning("langsmith not installed")
        return None
    if not os.getenv("LANGSMITH_API_KEY"):
        return None
    os.environ.setdefault("LANGCHAIN_TRACING_V2", "true")
    os.environ.setdefault("LANGCHAIN_PROJECT", os.getenv("LANGSMITH_PROJECT", "multimodal-rag"))
    return Client()


def traceable(name: str) -> Callable:
    """Wraps an async function so its inputs/outputs land in LangSmith as a span."""

    def deco(fn: Callable):
        try:
            from langsmith import traceable as _ls_traceable
        except Exception:
            return fn
        return _ls_traceable(name=name)(fn)

    return deco

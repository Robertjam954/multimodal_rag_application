"""Retry + fallback wrapper for flaky external calls.

Pattern lifted from langchain-ai/interrupt-resume-deep-agents/utils/search.py.
Wrap any async call that hits a remote service so an outage degrades gracefully
instead of breaking the whole `/chat` stream.

Usage:

    from core.resilience import resilient

    @resilient(name="ai_search", fallback=lambda *a, **kw: SearchResult.empty())
    async def search(...): ...

Or as a one-shot wrapper at the call site:

    result = await call_with_retry(
        lambda: client.search(query),
        name="ai_search",
        fallback=SearchResult.empty(),
    )
"""
from __future__ import annotations

import asyncio
import functools
import logging
from typing import Any, Awaitable, Callable, TypeVar

logger = logging.getLogger(__name__)

T = TypeVar("T")


async def call_with_retry(
    fn: Callable[[], Awaitable[T]],
    *,
    name: str,
    max_retries: int = 2,
    base_backoff_seconds: float = 1.0,
    fallback: T | Callable[[Exception], T] | None = None,
) -> T:
    """Call `fn` with linear backoff; on final failure return `fallback` or re-raise."""
    last_error: Exception | None = None
    for attempt in range(max_retries + 1):
        try:
            return await fn()
        except Exception as exc:
            last_error = exc
            if attempt < max_retries:
                wait = base_backoff_seconds * (attempt + 1)
                logger.warning("%s attempt %d failed (%s); retrying in %.1fs", name, attempt + 1, exc, wait)
                await asyncio.sleep(wait)

    logger.error("%s failed after %d attempts: %s", name, max_retries + 1, last_error)
    if fallback is None:
        assert last_error is not None
        raise last_error
    if callable(fallback):
        return fallback(last_error)  # type: ignore[arg-type]
    return fallback


def resilient(
    *,
    name: str,
    max_retries: int = 2,
    base_backoff_seconds: float = 1.0,
    fallback: Any = None,
):
    """Decorator form. See `call_with_retry`."""

    def decorator(fn: Callable[..., Awaitable[T]]) -> Callable[..., Awaitable[T]]:
        @functools.wraps(fn)
        async def wrapper(*args: Any, **kwargs: Any) -> T:
            return await call_with_retry(
                lambda: fn(*args, **kwargs),
                name=name,
                max_retries=max_retries,
                base_backoff_seconds=base_backoff_seconds,
                fallback=fallback,
            )

        return wrapper

    return decorator

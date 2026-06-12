"""Request decorators: auth, rate limit, ACL path check."""
from __future__ import annotations

import functools
import logging
import time
from collections import defaultdict
from typing import Any, Callable

from quart import current_app, request

from error import error_response

logger = logging.getLogger(__name__)

# In-memory token-bucket. Production should use Redis or a Cosmos record.
_BUCKETS: dict[str, list[float]] = defaultdict(list)


def _ip() -> str:
    return request.headers.get("X-Forwarded-For", request.remote_addr or "unknown").split(",")[0].strip()


def ratelimited(per_min: int | None = None) -> Callable:
    """Per-IP rate limiter. Reads RATE_LIMIT_PER_MIN if `per_min` is None."""

    def decorator(f: Callable):
        @functools.wraps(f)
        async def wrapper(*args, **kwargs):
            import os

            limit = per_min if per_min is not None else int(os.getenv("RATE_LIMIT_PER_MIN", "30"))
            now = time.time()
            window_start = now - 60
            ip = _ip()
            _BUCKETS[ip] = [t for t in _BUCKETS[ip] if t > window_start]
            if len(_BUCKETS[ip]) >= limit:
                return error_response("rate limit exceeded", code="rate_limited", status=429)
            _BUCKETS[ip].append(now)
            return await f(*args, **kwargs)

        return wrapper

    return decorator


def authenticated(f: Callable) -> Callable:
    """Optional MSAL auth. If AZURE_USE_AUTHENTICATION!=true, pass through."""

    @functools.wraps(f)
    async def wrapper(*args, **kwargs):
        import os

        if os.getenv("AZURE_USE_AUTHENTICATION", "false").lower() != "true":
            return await f(*args, **kwargs)
        from config import CONFIG_AUTH_CLIENT

        auth = current_app.config.get(CONFIG_AUTH_CLIENT)
        if auth is None:
            return error_response("auth not configured", code="auth_missing", status=401)
        claims = await auth.get_auth_claims_if_enabled(request.headers)
        if claims is None:
            return error_response("unauthorized", code="unauthorized", status=401)
        request.auth_claims = claims  # type: ignore[attr-defined]
        return await f(*args, **kwargs)

    return wrapper


def authenticated_path(f: Callable) -> Callable:
    """Like authenticated, but additionally checks that the requested path is in the user's ACL."""

    @functools.wraps(f)
    async def wrapper(*args, **kwargs):
        import os

        if os.getenv("AZURE_USE_AUTHENTICATION", "false").lower() != "true":
            return await f(*args, **kwargs)
        from config import CONFIG_AUTH_CLIENT

        auth = current_app.config.get(CONFIG_AUTH_CLIENT)
        if auth is None:
            return error_response("auth not configured", code="auth_missing", status=401)
        path = kwargs.get("path") or request.args.get("path", "")
        claims = await auth.check_path_auth(path, request.headers)
        if claims is None:
            return error_response("forbidden", code="forbidden", status=403)
        request.auth_claims = claims  # type: ignore[attr-defined]
        return await f(*args, **kwargs)

    return wrapper

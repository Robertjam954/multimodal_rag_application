"""State-based conversation memory backed by Redis.

Two stores per session, both keyed by `session_id`:

1. **Turn log** - an ordered Redis list of the most recent N message turns.
   Newest entries pushed at the head; capped via LTRIM. Each entry is a JSON
   blob `{role, content, ts}`. Used to feed conversation history into the next
   LLM call.

2. **Facts** - a Redis hash of stable preferences / facts the user has shared
   ("I work in Go", "prefer Postgres", "tenant is XYZ"). Updated explicitly by
   the agent when it extracts something worth keeping across sessions.

No-ops gracefully if `REDIS_URL` is unset, mirroring `SemanticCache`.

Env:
- CONVERSATION_MEMORY_INDEX        default "memory"
- CONVERSATION_MEMORY_MAX_TURNS    default 50
- CONVERSATION_MEMORY_TTL_SECONDS  default 2592000 (30 days)
"""
from __future__ import annotations

import json
import logging
import os
import time
from dataclasses import dataclass, field
from typing import Any

from core.semantic_cache import RedisCache

logger = logging.getLogger(__name__)


@dataclass
class Turn:
    role: str
    content: str
    ts: float = field(default_factory=time.time)

    def to_json(self) -> str:
        return json.dumps({"role": self.role, "content": self.content, "ts": self.ts})

    @classmethod
    def from_json(cls, blob: bytes | str) -> "Turn":
        data = json.loads(blob if isinstance(blob, str) else blob.decode("utf-8"))
        return cls(role=data["role"], content=data["content"], ts=float(data.get("ts", 0.0)))


def _ns() -> str:
    return os.getenv("CONVERSATION_MEMORY_INDEX", "memory")


def _max_turns() -> int:
    try:
        return max(1, int(os.getenv("CONVERSATION_MEMORY_MAX_TURNS", "50")))
    except ValueError:
        return 50


def _ttl_seconds() -> int:
    try:
        return max(60, int(os.getenv("CONVERSATION_MEMORY_TTL_SECONDS", "2592000")))
    except ValueError:
        return 2592000


def _turns_key(session_id: str) -> str:
    return f"{_ns()}:turns:{session_id}"


def _facts_key(session_id: str) -> str:
    return f"{_ns()}:facts:{session_id}"


class ConversationMemory:
    """Append-and-recall log of recent turns + a small key/value fact store per session."""

    @staticmethod
    async def remember(session_id: str, role: str, content: str) -> bool:
        """Append one turn. Trims oldest if the log exceeds `max_turns`."""
        cache = RedisCache.maybe()
        if cache is None or not session_id or not role or not content:
            return False
        try:
            key = _turns_key(session_id)
            turn = Turn(role=role, content=content)
            pipe = cache.client.pipeline()
            pipe.lpush(key, turn.to_json())
            pipe.ltrim(key, 0, _max_turns() - 1)
            pipe.expire(key, _ttl_seconds())
            await pipe.execute()
            return True
        except Exception:
            logger.exception("conversation_memory.remember failed")
            return False

    @staticmethod
    async def recall(session_id: str, k: int | None = None) -> list[Turn]:
        """Return the most recent `k` turns oldest-first (chat-ready order)."""
        cache = RedisCache.maybe()
        if cache is None or not session_id:
            return []
        try:
            key = _turns_key(session_id)
            limit = max(1, k) if k else _max_turns()
            # lpush + lrange 0..k-1 gives newest-first; reverse for chronological.
            raw = await cache.client.lrange(key, 0, limit - 1)
            turns = [Turn.from_json(r) for r in raw]
            turns.reverse()
            return turns
        except Exception:
            logger.exception("conversation_memory.recall failed")
            return []

    @staticmethod
    async def forget(session_id: str) -> bool:
        cache = RedisCache.maybe()
        if cache is None or not session_id:
            return False
        try:
            pipe = cache.client.pipeline()
            pipe.delete(_turns_key(session_id))
            pipe.delete(_facts_key(session_id))
            await pipe.execute()
            return True
        except Exception:
            logger.exception("conversation_memory.forget failed")
            return False


class UserFacts:
    """Small per-session key/value store for stable facts the agent has extracted."""

    @staticmethod
    async def set(session_id: str, key: str, value: str) -> bool:
        cache = RedisCache.maybe()
        if cache is None or not session_id or not key:
            return False
        try:
            hkey = _facts_key(session_id)
            await cache.client.hset(hkey, key, value)
            await cache.client.expire(hkey, _ttl_seconds())
            return True
        except Exception:
            logger.exception("user_facts.set failed")
            return False

    @staticmethod
    async def all(session_id: str) -> dict[str, str]:
        cache = RedisCache.maybe()
        if cache is None or not session_id:
            return {}
        try:
            raw = await cache.client.hgetall(_facts_key(session_id))
            return {
                (k.decode() if isinstance(k, bytes) else k): (v.decode() if isinstance(v, bytes) else v)
                for k, v in raw.items()
            }
        except Exception:
            logger.exception("user_facts.all failed")
            return {}

    @staticmethod
    async def delete(session_id: str, key: str) -> bool:
        cache = RedisCache.maybe()
        if cache is None or not session_id or not key:
            return False
        try:
            await cache.client.hdel(_facts_key(session_id), key)
            return True
        except Exception:
            logger.exception("user_facts.delete failed")
            return False


def messages_for_llm(turns: list[Turn], facts: dict[str, Any] | None = None) -> list[dict[str, str]]:
    """Convert recalled turns (+ optional facts preamble) into OpenAI-style messages."""
    out: list[dict[str, str]] = []
    if facts:
        fact_lines = "\n".join(f"- {k}: {v}" for k, v in facts.items())
        out.append({"role": "system", "content": f"Stable facts about this user:\n{fact_lines}"})
    for t in turns:
        if t.role in {"user", "assistant", "system"}:
            out.append({"role": t.role, "content": t.content})
    return out

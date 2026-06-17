"""Semantic FAQ cache + embedding cache on Redis Stack.

Two caches, one Redis connection:

1. SemanticCache - question embeddings indexed with HNSW; lookup by cosine
   similarity. Hit returns the cached answer payload (answer text, citations,
   verifier verdict). Reused across users only when ACL hashes match.

2. EmbeddingCache - SHA-256(model + text) -> embedding vector. Avoids re-embed
   when ingesting duplicate chunks or asking identical questions.

Both no-op when REDIS_URL is unset, so local dev without Redis still works.

Env vars:
- REDIS_URL                  redis://default:PASS@host:port  (required to enable)
- SEMANTIC_CACHE_THRESHOLD   default 0.93 (cosine similarity to count as hit)
- SEMANTIC_CACHE_TTL_SECONDS default 604800 (7 days)
- SEMANTIC_CACHE_INDEX       default "questions"
- EMBEDDING_CACHE_TTL_SECONDS default 2592000 (30 days)
"""
from __future__ import annotations

import hashlib
import json
import logging
import os
import struct
import time
from dataclasses import asdict, dataclass, field
from typing import Any

logger = logging.getLogger(__name__)


@dataclass
class CachedAnswer:
    question: str
    answer: str
    citations: list[dict[str, Any]] = field(default_factory=list)
    verdict: dict[str, Any] | None = None
    followups: list[str] = field(default_factory=list)
    model: str = ""
    acl_hash: str = ""
    ts: float = 0.0


def _vec_to_bytes(vec: list[float]) -> bytes:
    return struct.pack(f"{len(vec)}f", *vec)


def _bytes_to_vec(b: bytes) -> list[float]:
    n = len(b) // 4
    return list(struct.unpack(f"{n}f", b))


def _hash_text(model: str, text: str) -> str:
    h = hashlib.sha256()
    h.update(model.encode())
    h.update(b"\x00")
    h.update(text.encode())
    return h.hexdigest()


def _acl_hash(acl: dict[str, Any] | None) -> str:
    if not acl:
        return ""
    canon = json.dumps(acl, sort_keys=True).encode()
    return hashlib.sha256(canon).hexdigest()[:16]


class RedisCache:
    """Lazy Redis client + HNSW index setup. Single instance per process."""

    _instance: "RedisCache | None" = None

    def __init__(self, url: str) -> None:
        import redis.asyncio as redis  # local import so unset REDIS_URL doesn't force the dep

        self.url = url
        self.client = redis.from_url(url, decode_responses=False)
        self.threshold = float(os.getenv("SEMANTIC_CACHE_THRESHOLD", "0.93"))
        self.ttl_seconds = int(os.getenv("SEMANTIC_CACHE_TTL_SECONDS", "604800"))
        self.embedding_ttl_seconds = int(os.getenv("EMBEDDING_CACHE_TTL_SECONDS", "2592000"))
        self.index_name = os.getenv("SEMANTIC_CACHE_INDEX", "questions")
        self._index_ready = False
        self._embed_dim: int | None = None

    @classmethod
    def maybe(cls) -> "RedisCache | None":
        url = os.getenv("REDIS_URL")
        if not url:
            return None
        if cls._instance is None:
            try:
                cls._instance = cls(url)
            except Exception:
                logger.exception("Redis connection setup failed; caching disabled")
                return None
        return cls._instance

    async def _ensure_index(self, dim: int) -> None:
        if self._index_ready and self._embed_dim == dim:
            return
        # FT.CREATE is idempotent only when args match; we drop+recreate if dim drifts.
        try:
            from redis.commands.search.field import TagField, TextField, VectorField
            from redis.commands.search.index_definition import IndexDefinition, IndexType

            schema = (
                TextField("question"),
                TagField("acl_hash"),
                VectorField(
                    "embedding",
                    "HNSW",
                    {"TYPE": "FLOAT32", "DIM": dim, "DISTANCE_METRIC": "COSINE"},
                ),
            )
            try:
                await self.client.ft(self.index_name).info()
                # Index exists; trust the dim matches.
            except Exception:
                await self.client.ft(self.index_name).create_index(
                    schema,
                    definition=IndexDefinition(prefix=[f"{self.index_name}:"], index_type=IndexType.HASH),
                )
            self._index_ready = True
            self._embed_dim = dim
        except Exception:
            logger.exception("HNSW index setup failed; caching will be degraded")
            self._index_ready = False


class SemanticCache:
    """Question -> CachedAnswer via cosine similarity over question embeddings."""

    @staticmethod
    async def lookup(
        embedding: list[float],
        acl: dict[str, Any] | None = None,
    ) -> CachedAnswer | None:
        cache = RedisCache.maybe()
        if cache is None or not embedding:
            return None
        try:
            await cache._ensure_index(len(embedding))
            if not cache._index_ready:
                return None

            from redis.commands.search.query import Query

            acl_h = _acl_hash(acl)
            # KNN-1 with optional ACL filter; cosine distance => similarity = 1 - dist.
            filter_expr = f"@acl_hash:{{{acl_h or 'none'}}}"
            q = (
                Query(f"({filter_expr})=>[KNN 1 @embedding $vec AS dist]")
                .sort_by("dist")
                .return_fields("question", "answer_json", "dist")
                .dialect(2)
            )
            res = await cache.client.ft(cache.index_name).search(
                q, query_params={"vec": _vec_to_bytes(embedding)}
            )
            if not res.docs:
                return None
            doc = res.docs[0]
            dist = float(doc.dist)
            similarity = 1.0 - dist
            if similarity < cache.threshold:
                return None
            payload = json.loads(doc.answer_json)
            return CachedAnswer(**payload)
        except Exception:
            logger.exception("semantic cache lookup failed")
            return None

    @staticmethod
    async def store(
        question: str,
        embedding: list[float],
        answer: str,
        citations: list[dict[str, Any]] | None = None,
        verdict: dict[str, Any] | None = None,
        followups: list[str] | None = None,
        model: str = "",
        acl: dict[str, Any] | None = None,
    ) -> None:
        cache = RedisCache.maybe()
        if cache is None or not embedding or not answer:
            return
        try:
            await cache._ensure_index(len(embedding))
            if not cache._index_ready:
                return
            acl_h = _acl_hash(acl) or "none"
            payload = CachedAnswer(
                question=question,
                answer=answer,
                citations=citations or [],
                verdict=verdict,
                followups=followups or [],
                model=model,
                acl_hash=acl_h,
                ts=time.time(),
            )
            key = f"{cache.index_name}:{_hash_text('q', question)}:{acl_h}"
            await cache.client.hset(
                key,
                mapping={
                    "question": question,
                    "acl_hash": acl_h,
                    "embedding": _vec_to_bytes(embedding),
                    "answer_json": json.dumps(asdict(payload)),
                },
            )
            await cache.client.expire(key, cache.ttl_seconds)
        except Exception:
            logger.exception("semantic cache store failed")


class NotesIndex:
    """HNSW-indexed corpus of note chunks (separate index from the question cache).

    Layout (HASH per chunk):
        key                 = f"{prefix}:{note_id}:{chunk_index}"
        fields              = note_id, content, content_topic, source_url,
                              source_type, tags ('|'-joined), embedding (float32 bytes)
        index_name          = $NOTES_INDEX (default "notes")
        prefix              = f"{index_name}:"

    Coexists with `SemanticCache` (index `questions:`) on the same Redis client.
    """

    @staticmethod
    def _notes_index_name() -> str:
        return os.getenv("NOTES_INDEX", "notes")

    @classmethod
    async def _ensure_index(cls, dim: int) -> bool:
        cache = RedisCache.maybe()
        if cache is None:
            return False
        index_name = cls._notes_index_name()
        try:
            await cache.client.ft(index_name).info()
            return True
        except Exception:
            pass
        try:
            from redis.commands.search.field import TagField, TextField, VectorField
            from redis.commands.search.index_definition import IndexDefinition, IndexType

            schema = (
                TagField("note_id"),
                TextField("content"),
                TextField("content_topic"),
                TagField("source_url"),
                TagField("source_type"),
                TagField("tags", separator="|"),
                VectorField(
                    "embedding",
                    "HNSW",
                    {"TYPE": "FLOAT32", "DIM": dim, "DISTANCE_METRIC": "COSINE"},
                ),
            )
            await cache.client.ft(index_name).create_index(
                schema,
                definition=IndexDefinition(prefix=[f"{index_name}:"], index_type=IndexType.HASH),
            )
            return True
        except Exception:
            logger.exception("notes HNSW index setup failed")
            return False

    @staticmethod
    async def upsert_chunk(
        note_id: str,
        chunk_index: int,
        content: str,
        embedding: list[float],
        *,
        content_topic: str = "",
        source_url: str = "",
        source_type: str = "text",
        tags: list[str] | None = None,
    ) -> bool:
        cache = RedisCache.maybe()
        if cache is None or not embedding or not content:
            return False
        ok = await NotesIndex._ensure_index(len(embedding))
        if not ok:
            return False
        try:
            index_name = NotesIndex._notes_index_name()
            key = f"{index_name}:{note_id}:{chunk_index}"
            await cache.client.hset(
                key,
                mapping={
                    "note_id": note_id,
                    "content": content,
                    "content_topic": content_topic,
                    "source_url": source_url,
                    "source_type": source_type,
                    "tags": "|".join(tags or []),
                    "embedding": _vec_to_bytes(embedding),
                },
            )
            return True
        except Exception:
            logger.exception("notes upsert failed for note_id=%s chunk=%s", note_id, chunk_index)
            return False

    @staticmethod
    async def delete_note(note_id: str) -> int:
        cache = RedisCache.maybe()
        if cache is None:
            return 0
        try:
            index_name = NotesIndex._notes_index_name()
            pattern = f"{index_name}:{note_id}:*"
            deleted = 0
            async for key in cache.client.scan_iter(match=pattern, count=200):
                deleted += await cache.client.delete(key)
            return deleted
        except Exception:
            logger.exception("notes delete failed for note_id=%s", note_id)
            return 0

    @staticmethod
    async def search(
        embedding: list[float],
        *,
        top_k: int = 5,
        source_type: str | None = None,
        tag: str | None = None,
    ) -> list[dict[str, Any]]:
        """Vector top-k with optional metadata filters. Returns list of dicts with similarity."""
        cache = RedisCache.maybe()
        if cache is None or not embedding:
            return []
        ok = await NotesIndex._ensure_index(len(embedding))
        if not ok:
            return []
        try:
            from redis.commands.search.query import Query

            index_name = NotesIndex._notes_index_name()
            filters: list[str] = []
            if source_type:
                filters.append(f"@source_type:{{{source_type}}}")
            if tag:
                filters.append(f"@tags:{{{tag}}}")
            filter_expr = " ".join(filters) if filters else "*"
            q = (
                Query(f"({filter_expr})=>[KNN {top_k} @embedding $vec AS dist]")
                .sort_by("dist")
                .return_fields("note_id", "content", "content_topic", "source_url", "source_type", "tags", "dist")
                .paging(0, top_k)
                .dialect(2)
            )
            res = await cache.client.ft(index_name).search(
                q, query_params={"vec": _vec_to_bytes(embedding)}
            )
            out: list[dict[str, Any]] = []
            for doc in res.docs:
                payload = {f: getattr(doc, f, b"") for f in ("note_id", "content", "content_topic", "source_url", "source_type", "tags", "dist")}
                # bytes -> str where applicable
                for k, v in list(payload.items()):
                    if isinstance(v, bytes):
                        payload[k] = v.decode("utf-8", errors="replace")
                payload["similarity"] = 1.0 - float(payload.pop("dist", 1.0))
                tags_str = payload.pop("tags", "") or ""
                payload["tags"] = [t for t in tags_str.split("|") if t]
                out.append(payload)
            return out
        except Exception:
            logger.exception("notes search failed")
            return []


class NotesIngester:
    """Chunk + embed + upsert one note's worth of content into the NotesIndex."""

    @staticmethod
    async def ingest(
        content_topic: str,
        source_type: str,
        text: str,
        *,
        source_url: str = "",
        tags: list[str] | None = None,
        note_id: str | None = None,
        embed_fn: Any = None,
    ) -> dict[str, Any]:
        if source_type not in {"audio", "video", "text"}:
            raise ValueError(f"invalid source_type: {source_type!r}")
        if not text.strip():
            raise ValueError("text is required")

        from prepdocslib.textsplitter import split_text

        chunks = list(split_text(text)) or [text]

        # Default embed function uses the same Foundry client as Grok.
        if embed_fn is None:
            from core.embeddings_client import embed_texts

            embed_fn = embed_texts
        vectors = await embed_fn(chunks)
        if len(vectors) != len(chunks):
            raise RuntimeError(f"embed returned {len(vectors)} vectors for {len(chunks)} chunks")

        import uuid as _uuid

        nid = note_id or _uuid.uuid4().hex
        written = 0
        for i, (chunk, vec) in enumerate(zip(chunks, vectors)):
            ok = await NotesIndex.upsert_chunk(
                note_id=nid,
                chunk_index=i,
                content=chunk,
                embedding=vec,
                content_topic=content_topic,
                source_url=source_url,
                source_type=source_type,
                tags=tags or [],
            )
            if ok:
                written += 1
        return {"note_id": nid, "chunks": written, "content_topic": content_topic}


class EmbeddingCache:
    """SHA-256(model + text) -> packed float32 vector."""

    @staticmethod
    async def get_many(model: str, texts: list[str]) -> dict[int, list[float]]:
        """Return {index_in_input: vector} for cache hits."""
        cache = RedisCache.maybe()
        if cache is None or not texts:
            return {}
        try:
            keys = [f"emb:{_hash_text(model, t)}" for t in texts]
            pipe = cache.client.pipeline()
            for k in keys:
                pipe.get(k)
            raw_results = await pipe.execute()
            out: dict[int, list[float]] = {}
            for i, raw in enumerate(raw_results):
                if raw:
                    out[i] = _bytes_to_vec(raw)
            return out
        except Exception:
            logger.exception("embedding cache get failed")
            return {}

    @staticmethod
    async def set_many(model: str, texts: list[str], vectors: list[list[float]]) -> None:
        cache = RedisCache.maybe()
        if cache is None or not texts:
            return
        try:
            pipe = cache.client.pipeline()
            for t, v in zip(texts, vectors):
                if not v:
                    continue
                key = f"emb:{_hash_text(model, t)}"
                pipe.set(key, _vec_to_bytes(v), ex=cache.embedding_ttl_seconds)
            await pipe.execute()
        except Exception:
            logger.exception("embedding cache set failed")

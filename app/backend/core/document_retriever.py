"""Document retriever abstraction.

A `Retriever` knows how to turn a question into ranked `Document` objects pulled
from some store. Today there's one concrete implementation (Redis HNSW notes
index), but the interface lets a future swap (Azure AI Search, Cosmos vector,
hybrid BM25+dense, etc.) drop in without changing the agent or the tool layer.

Layers:
    LLM tool (search_notes)
        -> get_retriever().retrieve(query, k=..., source_type=..., tag=...)
            -> embed query, run HNSW KNN, return Documents
"""
from __future__ import annotations

import logging
import os
from dataclasses import dataclass, field
from functools import lru_cache
from typing import Any, Protocol

from core.embeddings_client import embed_one
from core.semantic_cache import NotesIndex

logger = logging.getLogger(__name__)


@dataclass
class Document:
    """A single retrieval hit. `content` is what the LLM reads; everything else is grounding metadata."""

    id: str
    content: str
    score: float
    source_url: str = ""
    source_type: str = "text"
    content_topic: str = ""
    tags: list[str] = field(default_factory=list)
    extra: dict[str, Any] = field(default_factory=dict)

    def to_citation(self) -> dict[str, Any]:
        """Compact dict the tool layer hands back to the LLM."""
        return {
            "note_id": self.id,
            "content_topic": self.content_topic,
            "source_url": self.source_url,
            "source_type": self.source_type,
            "tags": self.tags,
            "similarity": round(self.score, 4),
            "content": self.content[:600],
        }


class Retriever(Protocol):
    """Async retriever interface. Any backend that satisfies this can plug in."""

    name: str

    async def retrieve(
        self,
        query: str,
        *,
        k: int = 5,
        source_type: str | None = None,
        tag: str | None = None,
    ) -> list[Document]: ...

    async def get_document(self, doc_id: str) -> Document | None:
        """Return the full document (all chunks concatenated) by id, or None."""
        ...


class RedisNotesRetriever:
    """Vector retrieval over the Redis HNSW notes index.

    Embeds the query via the Foundry embedding deployment, then runs cosine KNN
    against the `notes:` index. Optional metadata filters narrow before KNN.
    """

    name = "redis_notes"

    async def retrieve(
        self,
        query: str,
        *,
        k: int = 5,
        source_type: str | None = None,
        tag: str | None = None,
    ) -> list[Document]:
        if not query.strip():
            return []
        k = max(1, min(int(k or 5), 25))
        try:
            qvec = await embed_one(query)
        except Exception:
            logger.exception("query embedding failed in RedisNotesRetriever")
            return []
        hits = await NotesIndex.search(qvec, top_k=k, source_type=source_type, tag=tag)
        return [
            Document(
                id=h["note_id"],
                content=h["content"],
                score=float(h["similarity"]),
                source_url=h.get("source_url", ""),
                source_type=h.get("source_type", "text"),
                content_topic=h.get("content_topic", ""),
                tags=list(h.get("tags", [])),
            )
            for h in hits
        ]

    async def get_document(self, doc_id: str) -> Document | None:
        """Walk all chunks for the given note_id in order and reassemble the full doc."""
        from core.semantic_cache import RedisCache

        cache = RedisCache.maybe()
        if cache is None or not doc_id:
            return None
        index_name = NotesIndex._notes_index_name()
        prefix = f"{index_name}:{doc_id}:"

        chunks: list[tuple[int, dict[str, Any]]] = []
        try:
            async for key in cache.client.scan_iter(match=f"{prefix}*", count=200):
                key_str = key.decode("utf-8") if isinstance(key, bytes) else key
                suffix = key_str[len(prefix):]
                try:
                    idx = int(suffix)
                except ValueError:
                    continue
                raw = await cache.client.hgetall(key)
                if not raw:
                    continue
                decoded = {
                    (k.decode() if isinstance(k, bytes) else k): v
                    for k, v in raw.items()
                }
                # Drop the embedding bytes; we don't need them and they're noisy.
                decoded.pop("embedding", None)
                # Decode text fields
                for f in ("note_id", "content", "content_topic", "source_url", "source_type", "tags"):
                    if isinstance(decoded.get(f), bytes):
                        decoded[f] = decoded[f].decode("utf-8", errors="replace")
                chunks.append((idx, decoded))
        except Exception:
            logger.exception("get_document scan failed for doc_id=%s", doc_id)
            return None

        if not chunks:
            return None

        chunks.sort(key=lambda x: x[0])
        first = chunks[0][1]
        full_content = "\n\n".join(c[1].get("content", "") for c in chunks if c[1].get("content"))
        tags_str = first.get("tags", "") or ""
        return Document(
            id=doc_id,
            content=full_content,
            score=1.0,
            source_url=first.get("source_url", ""),
            source_type=first.get("source_type", "text"),
            content_topic=first.get("content_topic", ""),
            tags=[t for t in tags_str.split("|") if t],
            extra={"chunk_count": len(chunks)},
        )


@lru_cache(maxsize=1)
def get_retriever() -> Retriever:
    """Process-wide retriever singleton.

    Selected by `DOCUMENT_RETRIEVER` env (default "redis_notes"). Add new
    implementations here as the project grows.
    """
    name = os.getenv("DOCUMENT_RETRIEVER", "redis_notes").lower()
    if name == "redis_notes":
        return RedisNotesRetriever()
    raise ValueError(f"unknown DOCUMENT_RETRIEVER: {name!r}")


def reset_retriever() -> None:
    get_retriever.cache_clear()

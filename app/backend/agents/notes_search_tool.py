"""`search_notes` - function-calling tool the tutor exposes to its LLM.

Thin wrapper around the `core.document_retriever.Retriever` interface so the
agent doesn't have to know which backend (Redis today, something else tomorrow)
is doing the retrieval.
"""
from __future__ import annotations

import logging
from typing import Any

from core.document_retriever import get_retriever

logger = logging.getLogger(__name__)


SEARCH_NOTES_SCHEMA: dict[str, Any] = {
    "type": "function",
    "function": {
        "name": "search_notes",
        "description": (
            "Semantic search over the AI engineering notes library (Redis HNSW). "
            "Call this whenever the user asks about a topic the notes likely cover - "
            "prompt caching, RAG retrieval/eval, verifiers, GraphRAG, NL-to-SQL, "
            "YouTube ingestion, etc. Returns up to `top_k` snippets with citations."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The user's information need, rephrased as a search query.",
                },
                "top_k": {
                    "type": "integer",
                    "description": "Number of snippets to return. Default 5, max 10.",
                    "default": 5,
                    "minimum": 1,
                    "maximum": 10,
                },
                "source_type": {
                    "type": "string",
                    "description": "Optional filter on note origin.",
                    "enum": ["audio", "video", "text"],
                },
                "tag": {
                    "type": "string",
                    "description": "Optional tag filter (e.g. 'retrieval', 'caching').",
                },
            },
            "required": ["query"],
            "additionalProperties": False,
        },
    },
}


GET_DOCUMENT_SCHEMA: dict[str, Any] = {
    "type": "function",
    "function": {
        "name": "get_document",
        "description": (
            "Fetch the full text of a single note (all chunks concatenated) by its "
            "note_id. Call this when the user asks to see the full document behind "
            "a citation, or when you need more context than the search snippet "
            "provided."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "note_id": {
                    "type": "string",
                    "description": "The note_id returned by search_notes (also shown in [note:<id>] citations).",
                },
            },
            "required": ["note_id"],
            "additionalProperties": False,
        },
    },
}


async def search_notes(
    query: str,
    top_k: int = 5,
    source_type: str | None = None,
    tag: str | None = None,
) -> dict[str, Any]:
    """Execute the tool. Returns a dict the agent feeds back as a tool message."""
    top_k = max(1, min(int(top_k or 5), 10))
    retriever = get_retriever()
    try:
        docs = await retriever.retrieve(query, k=top_k, source_type=source_type, tag=tag)
    except Exception as exc:  # noqa: BLE001
        logger.exception("retriever %s failed during search_notes", retriever.name)
        return {"error": f"retriever_failed: {exc}", "hits": []}

    return {
        "query": query,
        "top_k": top_k,
        "filters": {"source_type": source_type, "tag": tag},
        "retriever": retriever.name,
        "hit_count": len(docs),
        "hits": [d.to_citation() for d in docs],
    }


async def get_document(note_id: str) -> dict[str, Any]:
    """Fetch the full document for a note_id (all chunks reassembled)."""
    note_id = (note_id or "").strip()
    if not note_id:
        return {"error": "note_id is required"}
    retriever = get_retriever()
    try:
        doc = await retriever.get_document(note_id)
    except Exception as exc:  # noqa: BLE001
        logger.exception("retriever %s failed during get_document", retriever.name)
        return {"error": f"retriever_failed: {exc}"}
    if doc is None:
        return {"error": "not_found", "note_id": note_id}
    return {
        "note_id": doc.id,
        "content_topic": doc.content_topic,
        "source_url": doc.source_url,
        "source_type": doc.source_type,
        "tags": doc.tags,
        "chunk_count": doc.extra.get("chunk_count", 0),
        "content": doc.content,
    }

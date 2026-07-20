"""Retriever: parallel graph + file_search; rerank; build DataPoints."""
from __future__ import annotations

import asyncio
import logging
from typing import Any

from agents.tools import graph_search
from approaches.approach import Citation, DataPoints
from core.document_retriever import get_retriever

logger = logging.getLogger(__name__)


async def retrieve(
    question: str,
    overrides: dict[str, Any] | None = None,
    use_graphrag: bool = True,
    top: int = 5,
) -> DataPoints:
    overrides = overrides or {}
    k = overrides.get("top", top)

    # Primary retrieval: Cosmos NoSQL vector store (DOCUMENT_RETRIEVER=cosmos).
    retriever = get_retriever()
    docs_task = asyncio.create_task(retriever.retrieve(question, k=k))
    gr_task = (
        asyncio.create_task(graph_search(query=question, hops=overrides.get("graph_hops", 2), k=k))
        if use_graphrag
        else asyncio.create_task(_empty())
    )
    docs, gr = await asyncio.gather(docs_task, gr_task, return_exceptions=False)

    citations: list[Citation] = []
    text_snippets: list[str] = []

    for d in docs:
        citations.append(
            Citation(
                id=d.id,
                source_file=d.source_url or d.content_topic or "cosmos",
                source_page=None,
                score=d.score,
                content_snippet=(d.content or "")[:1500],
            )
        )
        text_snippets.append(d.content or "")

    subgraph = None
    if gr:
        subgraph = {"nodes": gr.get("nodes", []), "edges": gr.get("edges", [])}
        for chunk in gr.get("community_chunks", []):
            citations.append(
                Citation(
                    id=chunk["id"],
                    source_file=chunk.get("source", "graphrag-community"),
                    content_snippet=chunk.get("text", "")[:1500],
                )
            )
            text_snippets.append(chunk.get("text", ""))

    return DataPoints(text=text_snippets, citations=citations, graph_subgraph=subgraph)


async def _empty() -> dict[str, Any]:
    return {}

"""Retriever: parallel graph + file_search; rerank; build DataPoints."""
from __future__ import annotations

import asyncio
import logging
from typing import Any

from agents.tools import file_search, graph_search
from approaches.approach import Citation, DataPoints

logger = logging.getLogger(__name__)


async def retrieve(
    question: str,
    overrides: dict[str, Any] | None = None,
    use_graphrag: bool = True,
    top: int = 5,
) -> DataPoints:
    overrides = overrides or {}
    k = overrides.get("top", top)

    fs_task = asyncio.create_task(file_search(query=question, k=k))
    gr_task = (
        asyncio.create_task(graph_search(query=question, hops=overrides.get("graph_hops", 2), k=k))
        if use_graphrag
        else asyncio.create_task(_empty())
    )
    fs, gr = await asyncio.gather(fs_task, gr_task, return_exceptions=False)

    citations: list[Citation] = []
    text_snippets: list[str] = []

    for r in fs:
        cid = r.get("id") or r.get("annotation_id") or r.get("filename", "?")
        citations.append(
            Citation(
                id=cid,
                source_file=r.get("filename", "unknown"),
                source_page=str(r.get("page")) if r.get("page") else None,
                score=r.get("score"),
                content_snippet=r.get("content", "")[:1500],
            )
        )
        text_snippets.append(r.get("content", ""))

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

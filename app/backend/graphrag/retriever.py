"""GraphRAG retrieval modes: local, global, drift, hybrid.

- local: BFS expand around top-k entity matches
- global: scan community summaries
- drift: iterative LLM-guided traversal
- hybrid: local + global merged
"""
from __future__ import annotations

import logging
from typing import Any

from graphrag import community, cosmos_gremlin

logger = logging.getLogger(__name__)


async def local_search(query: str, k: int = 5) -> dict[str, Any]:
    """BFS-expand around entities that match the query string."""
    g = cosmos_gremlin.CosmosGremlin()
    seeds = await g.neighbors(node_id=query, hops=1)  # naive seed; real impl does entity match
    return {"nodes": seeds.get("nodes", [])[:k], "edges": seeds.get("edges", [])[:k * 2], "community_chunks": []}


async def global_search(query: str, k: int = 5) -> dict[str, Any]:
    """Use community summaries as virtual chunks."""
    chunks = community.load()
    ranked = chunks[:k]  # naive; real impl scores by embedding similarity
    return {
        "nodes": [],
        "edges": [],
        "community_chunks": [{"id": c["id"], "text": c["summary"], "source": "graphrag-community"} for c in ranked],
    }


async def drift_search(query: str, hops: int = 3, k: int = 5) -> dict[str, Any]:
    """LLM-guided iterative traversal. Stub for now."""
    return await local_search(query, k=k)


async def hybrid_search(query: str, hops: int = 2, k: int = 5) -> dict[str, Any]:
    import asyncio

    local, glob = await asyncio.gather(local_search(query, k=k), global_search(query, k=k))
    return {
        "nodes": local["nodes"] + glob["nodes"],
        "edges": local["edges"] + glob["edges"],
        "community_chunks": local["community_chunks"] + glob["community_chunks"],
    }

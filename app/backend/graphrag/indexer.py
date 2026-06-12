"""Drives GraphRAG offline indexing for a corpus of chunks.

For each chunk:
1) entity_extractor.extract -> nodes + edges
2) cosmos_gremlin upserts
3) After all chunks: community.refresh
"""
from __future__ import annotations

import logging
from typing import Any

from graphrag import community, cosmos_gremlin, entity_extractor

logger = logging.getLogger(__name__)


async def index_chunks(chunks: list[dict[str, Any]]) -> dict[str, Any]:
    gremlin = cosmos_gremlin.CosmosGremlin()
    all_edges: list[dict[str, Any]] = []
    n_nodes = n_edges = 0
    for ch in chunks:
        kg = await entity_extractor.extract(ch.get("content", ""), source_id=ch.get("id"))
        for node in kg.get("nodes", []):
            await gremlin.upsert_node(node["id"], node.get("label", "Entity"), node.get("properties", {}))
            n_nodes += 1
        for edge in kg.get("edges", []):
            await gremlin.upsert_edge(edge["source"], edge["target"], edge.get("label", "REL"), edge.get("properties"))
            all_edges.append(edge)
            n_edges += 1
    n_communities = await community.refresh(all_edges)
    return {"nodes": n_nodes, "edges": n_edges, "communities": n_communities}

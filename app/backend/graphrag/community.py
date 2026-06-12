"""GraphRAG community summaries: Leiden communities + LLM-generated summary per community."""
from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

COMMUNITIES_PATH = Path(__file__).parent / "_communities.jsonl"


async def refresh(graph_edges: list[dict[str, Any]] | None = None) -> int:
    """Recompute community summaries. Returns number of communities written."""
    try:
        import networkx as nx
    except Exception:
        logger.warning("networkx not installed; skip community refresh")
        return 0

    g = nx.Graph()
    for e in graph_edges or []:
        g.add_edge(e["source"], e["target"], label=e.get("label", ""))
    if g.number_of_nodes() == 0:
        return 0

    try:
        from networkx.algorithms.community import louvain_communities

        communities = louvain_communities(g, seed=42)
    except Exception:
        communities = [set(g.nodes())]

    from agents._llm import complete

    lines: list[str] = []
    for i, comm in enumerate(communities):
        subnodes = list(comm)[:40]
        summary = await complete(
            system="Summarize this graph community in 2-3 sentences. No markdown.",
            user=f"Nodes: {subnodes}",
            temperature=0.2,
        )
        lines.append(json.dumps({"id": f"community-{i}", "nodes": subnodes, "summary": summary}))
    COMMUNITIES_PATH.write_text("\n".join(lines))
    return len(communities)


def load() -> list[dict[str, Any]]:
    if not COMMUNITIES_PATH.exists():
        return []
    return [json.loads(line) for line in COMMUNITIES_PATH.read_text().splitlines() if line.strip()]

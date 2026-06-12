"""Seed Cosmos Gremlin with a small sample graph for the Voice + Papers demos."""
from __future__ import annotations

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "app" / "backend"))

from graphrag.cosmos_gremlin import CosmosGremlin  # noqa: E402


SAMPLE = {
    "nodes": [
        {"id": "Paper:demo-1", "label": "Paper", "properties": {"title": "Sample Paper"}},
        {"id": "Author:demo-a", "label": "Author", "properties": {"name": "Jane Doe"}},
        {"id": "Recording:demo-r", "label": "Recording", "properties": {"name": "Lab meeting 1"}},
        {"id": "Speaker:demo-s", "label": "Speaker", "properties": {"name": "Speaker 1"}},
    ],
    "edges": [
        {"source": "Author:demo-a", "target": "Paper:demo-1", "label": "AUTHORED"},
        {"source": "Speaker:demo-s", "target": "Recording:demo-r", "label": "SPEAKS"},
    ],
}


async def main() -> int:
    g = CosmosGremlin()
    for n in SAMPLE["nodes"]:
        await g.upsert_node(n["id"], n["label"], n["properties"])
    for e in SAMPLE["edges"]:
        await g.upsert_edge(e["source"], e["target"], e["label"])
    print("seeded")
    return 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))

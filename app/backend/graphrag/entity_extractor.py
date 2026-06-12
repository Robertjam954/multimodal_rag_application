"""Entity + relation extraction over chunked text.

Output schema:
- nodes: [{id, label, properties}]
- edges: [{source, target, label, properties}]

Labels: Paper | Section | Figure | Author | Citation | Recording | Utterance | Speaker | Topic
"""
from __future__ import annotations

import json
import logging
from typing import Any

from agents._llm import complete

logger = logging.getLogger(__name__)

EXTRACT_SYSTEM = """Extract a knowledge graph from the text. Output JSON with two keys:
nodes (list of {id, label, properties}) and edges (list of {source, target, label, properties}).
Use only these labels for nodes: Paper, Section, Figure, Author, Citation, Recording, Utterance, Speaker, Topic.
Use only these labels for edges: AUTHORED, CONTAINS, CITES, MENTIONS, SPEAKS, ABOUT.
JSON only."""


async def extract(text: str, source_id: str | None = None) -> dict[str, Any]:
    user = f"Source: {source_id or 'unknown'}\n\nText:\n{text[:6000]}"
    raw = await complete(system=EXTRACT_SYSTEM, user=user, temperature=0.0)
    start, end = raw.find("{"), raw.rfind("}")
    try:
        return json.loads(raw[start : end + 1]) if start != -1 else {"nodes": [], "edges": []}
    except Exception:
        logger.warning("entity_extractor JSON parse failed")
        return {"nodes": [], "edges": []}

"""Tool implementations shared by all agents.

- file_search: OpenAI Responses API file_search (citation-grade)
- graph_search: GraphRAG local + community retrieval
- verify_claim_tool: thin wrapper around verifier.verify_claim
- sql_plan: SchemaFlow approach entrypoint

Each function returns plain dicts / list[dict] so it can be exposed as an LLM tool.
"""
from __future__ import annotations

import logging
import os
from typing import Any

logger = logging.getLogger(__name__)


async def file_search(query: str, k: int = 5) -> list[dict[str, Any]]:
    """OpenAI Responses API file_search. Falls back to a stub if not configured."""
    vs_id = os.getenv("OPENAI_FILE_SEARCH_VECTOR_STORE_ID")
    api_key = os.getenv("OPENAI_API_KEY")
    if not (vs_id and api_key):
        logger.info("file_search stub path (no vector store id / key)")
        return [
            {
                "id": "stub-1",
                "filename": "sample_paper.pdf",
                "page": 1,
                "score": 0.95,
                "content": "Stubbed paper content. Configure OPENAI_FILE_SEARCH_VECTOR_STORE_ID to enable.",
            }
        ]
    from openai import AsyncOpenAI

    client = AsyncOpenAI(api_key=api_key)
    resp = await client.responses.create(
        model=os.getenv("OPENAI_FILE_SEARCH_MODEL", "gpt-4.1-mini"),
        tools=[{"type": "file_search", "vector_store_ids": [vs_id], "max_num_results": k}],
        input=query,
    )
    out: list[dict[str, Any]] = []
    for item in resp.output or []:
        if getattr(item, "type", None) == "file_search_call":
            for r in (getattr(item, "results", None) or []):
                out.append(
                    {
                        "id": getattr(r, "file_id", None) or getattr(r, "id", None),
                        "filename": getattr(r, "filename", None),
                        "page": getattr(r, "page", None),
                        "score": getattr(r, "score", None),
                        "content": getattr(r, "text", None) or "",
                    }
                )
    return out


async def graph_search(query: str, hops: int = 2, k: int = 5) -> dict[str, Any]:
    """GraphRAG hybrid local + community retrieval. Falls back to stub if no Cosmos endpoint."""
    if not os.getenv("AZURE_COSMOSDB_ACCOUNT"):
        logger.info("graph_search stub path (no cosmos account)")
        return {
            "nodes": [{"id": "Paper:stub", "label": "Paper", "title": "Sample paper"}],
            "edges": [],
            "community_chunks": [
                {"id": "community-1", "source": "graphrag-community", "text": f"Community summary for query '{query}'."}
            ],
        }
    try:
        from graphrag.retriever import hybrid_search

        return await hybrid_search(query=query, hops=hops, k=k)
    except Exception:
        logger.exception("graph_search failed; returning empty result")
        return {"nodes": [], "edges": [], "community_chunks": []}


async def verify_claim_tool(claim_sentence: str, evidence_ids: list[str]) -> dict[str, Any]:
    """Wrap verifier so it can be exposed as an LLM tool to the agent graph."""
    from agents.verifier import verify_claim
    from approaches.approach import Citation, Claim, DataPoints

    dp = DataPoints(citations=[Citation(id=eid, source_file="?") for eid in evidence_ids])
    verdict = await verify_claim(Claim(sentence=claim_sentence, citation_ids=evidence_ids), dp)
    return {"label": verdict.label, "reason": verdict.reason}


# ---- OpenAI / Foundry tool schemas (for hosted agents) ----

OPENAI_TOOL_DEFINITIONS = [
    {
        "type": "function",
        "function": {
            "name": "file_search",
            "description": "Search the OpenAI file_search vector store for evidence chunks.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string"},
                    "k": {"type": "integer", "default": 5},
                },
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "graph_search",
            "description": "Search the GraphRAG knowledge graph (local + community).",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string"},
                    "hops": {"type": "integer", "default": 2},
                    "k": {"type": "integer", "default": 5},
                },
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "verify_claim",
            "description": "Verify whether the given evidence supports the claim.",
            "parameters": {
                "type": "object",
                "properties": {
                    "claim_sentence": {"type": "string"},
                    "evidence_ids": {"type": "array", "items": {"type": "string"}},
                },
                "required": ["claim_sentence", "evidence_ids"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "sql_plan",
            "description": "Plan a SQL schema change using the SchemaFlow multi-agent pipeline.",
            "parameters": {
                "type": "object",
                "properties": {"change_request": {"type": "string"}},
                "required": ["change_request"],
            },
        },
    },
]

"""Azure skills - LangChain tool wrappers bound to the hierarchical-team agents.

Each skill is a thin ``@tool`` adapter over an existing async implementation
(``agents.tools``, ``agents.notes_search_tool``, the SchemaFlow approach, or the
Azure AI Search SDK). No business logic is duplicated here; the wrappers exist so
LangGraph ``create_react_agent`` workers can call the app's Azure services as
real bound tools.

Skills degrade to the same stubs their underlying functions already return when
the corresponding Azure environment is not configured, so they stay offline-safe
for tests.

Grouped exports:
- ``RETRIEVAL_SKILLS`` - bound to the Retrieval team workers.
- ``ANSWER_SKILLS``    - bound to the Answer/Verify team workers.
- ``SQL_SKILLS``       - bound to the SchemaFlow SQL sub-team worker.
"""
from __future__ import annotations

import json
import logging
import os
from typing import Any

from langchain_core.tools import tool

logger = logging.getLogger(__name__)


# ---- Retrieval skills -------------------------------------------------------


@tool
async def file_search_skill(query: str, k: int = 5) -> str:
    """Search the OpenAI file_search vector store for citation-grade evidence chunks.

    Use for direct quotes and page-anchored citations from ingested papers.
    Returns a JSON list of {id, filename, page, score, content}.
    """
    from agents.tools import file_search

    return json.dumps(await file_search(query=query, k=k))


@tool
async def azure_ai_search_skill(query: str, top: int = 5) -> str:
    """Hybrid (vector + semantic) search over the primary Azure AI Search index.

    This is the canonical RAG retrieval path for the corpus. Use for broad topical
    recall. Returns a JSON list of {id, source_file, page, score, content}.
    """
    service = os.getenv("AZURE_SEARCH_SERVICE")
    index = os.getenv("AZURE_SEARCH_INDEX")
    if not (service and index):
        logger.info("azure_ai_search stub path (no AZURE_SEARCH_SERVICE / AZURE_SEARCH_INDEX)")
        return json.dumps(
            [
                {
                    "id": "search-stub-1",
                    "source_file": "sample_paper.pdf",
                    "page": 1,
                    "score": 0.9,
                    "content": "Stubbed AI Search hit. Set AZURE_SEARCH_SERVICE + AZURE_SEARCH_INDEX to enable.",
                }
            ]
        )
    try:
        from azure.identity.aio import DefaultAzureCredential
        from azure.search.documents.aio import SearchClient
        from azure.search.documents.models import QueryType

        async with DefaultAzureCredential() as cred, SearchClient(
            endpoint=f"https://{service}.search.windows.net",
            index_name=index,
            credential=cred,
        ) as client:
            results = await client.search(
                search_text=query,
                top=top,
                query_type=QueryType.SEMANTIC,
                semantic_configuration_name=os.getenv("AZURE_SEARCH_SEMANTIC_CONFIG", "default"),
            )
            out: list[dict[str, Any]] = []
            async for doc in results:
                out.append(
                    {
                        "id": doc.get("id") or doc.get("chunk_id") or doc.get("sourcepage", "?"),
                        "source_file": doc.get("sourcefile") or doc.get("sourcepage", "unknown"),
                        "page": doc.get("page"),
                        "score": doc.get("@search.score"),
                        "content": (doc.get("content") or "")[:1500],
                    }
                )
            return json.dumps(out)
    except Exception:
        logger.exception("azure_ai_search failed; returning empty result")
        return json.dumps([])


@tool
async def graph_search_skill(query: str, hops: int = 2, k: int = 5) -> str:
    """Search the GraphRAG knowledge graph (Cosmos Gremlin local + community summaries).

    Use for multi-hop / relational questions that span entities. Returns a JSON
    object {nodes, edges, community_chunks}.
    """
    from agents.tools import graph_search

    return json.dumps(await graph_search(query=query, hops=hops, k=k))


@tool
async def notes_search_skill(
    query: str,
    top_k: int = 5,
    source_type: str | None = None,
    tag: str | None = None,
) -> str:
    """Semantic search over the AI-engineering notes library (Redis HNSW).

    Use for tutor-style questions about notes (RAG, caching, verifiers, GraphRAG,
    NL-to-SQL, ingestion). Returns a JSON object with `hits` and citations.
    """
    from agents.notes_search_tool import search_notes

    return json.dumps(await search_notes(query=query, top_k=top_k, source_type=source_type, tag=tag))


@tool
async def get_document_skill(note_id: str) -> str:
    """Fetch the full text of a single note (all chunks reassembled) by its note_id.

    Use when a search snippet is insufficient and the full document is needed.
    Returns a JSON object with the document content and metadata.
    """
    from agents.notes_search_tool import get_document

    return json.dumps(await get_document(note_id=note_id))


# ---- Answer / Verify skills -------------------------------------------------


@tool
async def verify_claim_skill(claim_sentence: str, evidence_ids: list[str]) -> str:
    """Verify whether the cited evidence supports a claim sentence.

    Returns a JSON object {label: supported|unsupported, reason}.
    """
    from agents.tools import verify_claim_tool

    return json.dumps(await verify_claim_tool(claim_sentence=claim_sentence, evidence_ids=evidence_ids))


# ---- SQL skills -------------------------------------------------------------


@tool
async def sql_plan_skill(change_request: str) -> str:
    """Plan a SQL schema change with the SchemaFlow pipeline (Parse/Impact/Plan/SQL).

    Use for NL-to-SQL warehouse change requests. Returns a JSON bundle with the
    parsed request, impact analysis, rollout plan, layered SQL, and validation.
    """
    from approaches.sql_schemaflow_approach import SchemaFlowSQLApproach

    bundle = await SchemaFlowSQLApproach().run_for_question(change_request)
    return json.dumps(bundle)


# ---- Grouped exports --------------------------------------------------------

RETRIEVAL_SKILLS = [
    file_search_skill,
    azure_ai_search_skill,
    graph_search_skill,
    notes_search_skill,
    get_document_skill,
]

ANSWER_SKILLS = [verify_claim_skill]

SQL_SKILLS = [sql_plan_skill]

ALL_SKILLS = [*RETRIEVAL_SKILLS, *ANSWER_SKILLS, *SQL_SKILLS]

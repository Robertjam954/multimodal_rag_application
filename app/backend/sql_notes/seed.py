"""Seed the blog-notes DB with a handful of AI-engineering notes so the demo works on first run.

Idempotent: rows are only inserted if their `content_topic` does not already exist.

    python -m sql_notes.seed
"""
from __future__ import annotations

import asyncio
import logging
from typing import Any

from sql_notes.connector import get_db

logger = logging.getLogger(__name__)

SAMPLE_NOTES: list[dict[str, Any]] = [
    {
        "content_topic": "Prompt caching cuts repeat-context costs by an order of magnitude",
        "hook_intro": "Most production RAG systems re-send the same system prompt and tool definitions every call. Prompt caching turns that fixed-cost overhead into a near-zero rebill.",
        "key_insights": [
            "Cache hits are billed at ~10% of fresh-prompt input cost.",
            "Cache TTL is 5 minutes - bundle reads inside a single user turn to maximize reuse.",
            "Reorder the prompt so cacheable content sits before per-request content.",
        ],
        "seo_keywords": ["prompt caching", "RAG cost optimization", "Anthropic cache control"],
        "source_url": "https://example.com/notes/prompt-caching",
        "source_type": "text",
        "tags": ["caching", "cost", "anthropic"],
    },
    {
        "content_topic": "Hybrid retrieval beats dense-only on long-tail technical queries",
        "hook_intro": "Embeddings collapse rare jargon into the manifold of common usage. BM25 still finds the exact-match needle.",
        "key_insights": [
            "Reciprocal-rank fusion is the cheapest hybrid baseline.",
            "Reweight BM25 when query length is short or domain-specific.",
            "Dense-only ranks API names below their description text.",
        ],
        "seo_keywords": ["hybrid search", "BM25", "reciprocal rank fusion", "RAG retrieval"],
        "source_url": "https://example.com/notes/hybrid-retrieval",
        "source_type": "text",
        "tags": ["retrieval", "bm25", "rrf"],
    },
    {
        "content_topic": "Evaluating RAG with promptfoo + LLM-as-judge",
        "hook_intro": "Manual eval doesn't scale past a hundred questions. LLM-as-judge does, with the right rubric.",
        "key_insights": [
            "Use a different judge model than the answerer to avoid self-preference bias.",
            "Anchor the rubric with explicit pass/fail examples.",
            "Run the same eval at every PR to catch regressions before merge.",
        ],
        "seo_keywords": ["RAG evaluation", "LLM as judge", "promptfoo"],
        "source_url": "https://example.com/notes/rag-eval",
        "source_type": "text",
        "tags": ["evaluation", "promptfoo"],
    },
    {
        "content_topic": "Verifier agents catch unsupported claims before they reach the user",
        "hook_intro": "Generation hallucinates. Retrieval is fallible. A verifier sits between them and refuses to ship sentences that no citation supports.",
        "key_insights": [
            "Run verification claim-by-claim, not on the whole answer.",
            "Treat an unsupported claim as a retrieval miss, not a generation bug - retry with broader top_k.",
            "Stream verdicts alongside tokens so the UI can gray out unverified sentences live.",
        ],
        "seo_keywords": ["verifier agent", "grounding", "hallucination mitigation"],
        "source_url": "https://example.com/notes/verifier",
        "source_type": "text",
        "tags": ["verifier", "grounding"],
    },
    {
        "content_topic": "GraphRAG turns scattered notes into a navigable knowledge graph",
        "hook_intro": "Chunk-based retrieval misses the connective tissue. GraphRAG materializes the edges the chunker dropped.",
        "key_insights": [
            "Local search answers entity-anchored questions; global search answers themes.",
            "Community summaries make the global query cheap.",
            "Refresh communities after every ingestion batch or they go stale fast.",
        ],
        "seo_keywords": ["GraphRAG", "knowledge graph", "community detection"],
        "source_url": "https://example.com/notes/graphrag",
        "source_type": "text",
        "tags": ["graphrag", "retrieval"],
    },
    {
        "content_topic": "Schema-aware NL->SQL agents are bounded by the schema you feed them",
        "hook_intro": "The model can't query a column it has never seen. Inject the live DDL on every call - even if it feels wasteful.",
        "key_insights": [
            "Introspect the schema at request time, not at deploy time.",
            "Reject any statement that isn't a single SELECT or WITH.",
            "Cap the row count server-side - the LLM cannot.",
        ],
        "seo_keywords": ["NL to SQL", "text to SQL", "agent safety"],
        "source_url": "https://example.com/notes/nl-to-sql",
        "source_type": "text",
        "tags": ["sql", "agents"],
    },
    {
        "content_topic": "YouTube transcripts are the cheapest tutorial corpus you can get",
        "hook_intro": "Most AI engineering teaching lives on YouTube. The transcript API is free, segmented, and timestamp-aligned.",
        "key_insights": [
            "Each segment carries a start time - keep it so citations can deep-link.",
            "The third-party transcript library rate-limits aggressively; retry with backoff.",
            "Re-chunk segments before embedding - raw segments are too short.",
        ],
        "seo_keywords": ["YouTube transcript", "video ingestion", "RAG corpus"],
        "source_url": "https://example.com/notes/youtube",
        "source_type": "video",
        "tags": ["ingestion", "video", "youtube"],
    },
]


async def seed() -> int:
    db = get_db()
    inserted = 0
    async with db.connection() as conn:
        for note in SAMPLE_NOTES:
            cur = await conn.execute(
                "SELECT id FROM blog_notes WHERE content_topic = ?",
                (note["content_topic"],),
            )
            if await cur.fetchone():
                continue
            note_id = await db.insert_note(**note)
            logger.info("inserted note id=%s topic=%r", note_id, note["content_topic"])
            inserted += 1
    return inserted


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    inserted = asyncio.run(seed())
    print(f"seeded {inserted} new note(s)")


if __name__ == "__main__":
    main()

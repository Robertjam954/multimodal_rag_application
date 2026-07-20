"""Single-pass RAG approach (kept for parity with azure-search-openai-demo).

The full multi-agent loop is in multiagent_approach.py. This one is used for the
`/chat/nonstream` baseline and as a fallback if Verifier is disabled.
"""
from __future__ import annotations

import logging
from typing import Any

from approaches.approach import Approach, DataPoints

logger = logging.getLogger(__name__)


class ChatReadRetrieveReadApproach(Approach):
    """Classic ReadRetrieveRead pattern: query rewrite -> retrieve -> answer."""

    async def run(
        self,
        messages: list[dict[str, Any]],
        context: dict[str, Any] | None = None,
        session_state: str | None = None,
    ) -> dict[str, Any]:
        overrides = (context or {}).get("overrides", {})
        question = messages[-1]["content"] if messages else ""

        # Query rewrite
        rewritten = await self._rewrite_query(question, messages, overrides)

        # Retrieve from the Cosmos NoSQL vector store (DOCUMENT_RETRIEVER=cosmos).
        from core.document_retriever import get_retriever

        docs = await get_retriever().retrieve(rewritten, k=overrides.get("top", 5))
        text_results = [{"content": d.content} for d in docs]
        evidence = DataPoints(text=[d.content for d in docs], citations=[])

        # Answer (no Verifier here; that path is in MultiAgentApproach)
        from agents.answerer import answer

        answer_text, claims, citations = await answer(
            question=question,
            evidence=evidence,
            messages=messages,
            prompt_manager=self.prompt_manager,
            overrides=overrides,
            stream=False,
        )

        return {
            "answer": answer_text,
            "claims": [c.__dict__ for c in claims],
            "citations": [c.__dict__ for c in citations],
            "thought_process": [
                {"title": "query_rewrite", "description": rewritten},
                {"title": "retrieval", "description": f"{len(text_results)} hits"},
            ],
            "session_state": session_state,
        }

    async def _rewrite_query(self, question: str, messages: list[dict[str, Any]], overrides: dict[str, Any]) -> str:
        if not self.prompt_manager:
            return question
        try:
            self.prompt_manager.render("query_rewrite.system.jinja2", history=messages[:-1])
        except Exception:
            logger.debug("query_rewrite template missing; using raw question")
        return question

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

        # Retrieve
        from agents.tools import file_search, graph_search

        text_results = await file_search(query=rewritten, k=overrides.get("top", 5))
        evidence = DataPoints(text=[r["content"] for r in text_results], citations=[])

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

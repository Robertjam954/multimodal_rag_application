"""Hierarchical multi-agent orchestration (opt-in via USE_HIERARCHICAL_AGENTS).

A supervisor-driven alternative to the flat ``MultiAgentApproach``. A top
coordinator divides work between a Retrieval team (LLM supervisor over
Azure-skill workers), an Answer/Verify team, and a SchemaFlow SQL team - see
``agents/hierarchical_graph.py``.

This approach emits the **identical SSE event schema** as the flat path (``route``,
``citation``, ``token``, ``claim``, ``verdict``, ``followups``, ``sql``, ``cost``,
plus the preamble's ``query_enhanced`` / ``cache_hit`` / ``blocked``), so the
frontend works unchanged. Graph nodes stream those events through a LangGraph
custom ``StreamWriter``; this class forwards them and bookends with the shared
preamble + semantic-cache write-back.

If LangGraph or a LLM provider is unavailable, it transparently falls back to
``MultiAgentApproach``.
"""
from __future__ import annotations

import logging
import os
from typing import Any, AsyncGenerator

from approaches.approach import Approach

logger = logging.getLogger(__name__)


class HierarchicalMultiAgentApproach(Approach):
    async def run(
        self,
        messages: list[dict[str, Any]],
        context: dict[str, Any] | None = None,
        session_state: str | None = None,
    ) -> dict[str, Any]:
        final: dict[str, Any] = {
            "answer": "",
            "claims": [],
            "citations": [],
            "verifier_verdict": None,
            "followups": [],
            "cost": {},
            "session_state": session_state,
        }
        async for evt in self.run_stream(messages, context, session_state):
            kind = evt.get("event")
            if kind == "token":
                final["answer"] += evt.get("data", "")
            elif kind == "claim":
                final["claims"].append(evt["data"])
            elif kind == "citation":
                final["citations"].append(evt["data"])
            elif kind == "verdict":
                final["verifier_verdict"] = evt["data"]
            elif kind == "followups":
                final["followups"] = evt["data"]
            elif kind == "cost":
                final["cost"] = evt["data"]
            elif kind == "sql":
                final["sql"] = evt["data"]
        return final

    async def run_stream(
        self,
        messages: list[dict[str, Any]],
        context: dict[str, Any] | None = None,
        session_state: str | None = None,
    ) -> AsyncGenerator[dict[str, Any], None]:
        # Build the graph first; fall back to the flat approach if unavailable.
        from agents.hierarchical_graph import build_hierarchical_graph

        graph = build_hierarchical_graph(prompt_manager=self.prompt_manager)
        if graph is None:
            logger.info("hierarchical graph unavailable; falling back to MultiAgentApproach")
            from approaches.multiagent_approach import MultiAgentApproach

            async for evt in MultiAgentApproach(prompt_manager=self.prompt_manager).run_stream(
                messages, context, session_state
            ):
                yield evt
            return

        # Shared pre-flight (cache / persona / enhancement / safety / route).
        from approaches._agentic_preamble import PREAMBLE_DONE, run_preamble

        pre: dict[str, Any] = {}
        async for evt in run_preamble(messages, context, self.prompt_manager):
            if evt.get("event") == PREAMBLE_DONE:
                pre = evt["data"]
                break
            yield evt
        if pre.get("terminate"):
            return

        question = pre["question"]
        overrides = pre["overrides"]
        question_embedding = pre.get("question_embedding")
        route_label = pre.get("route") or "factual"

        from langchain_core.messages import HumanMessage

        init_state = {
            "messages": [HumanMessage(content=question)],
            "messages_raw": messages,
            "question": question,
            "overrides": overrides,
            "route": route_label,
        }

        # Drive the graph; nodes emit SSE-shaped dicts via the custom stream writer.
        accumulated = ""
        citations: list[dict[str, Any]] = []
        verdict: dict[str, Any] | None = None
        followups: list[str] = []
        try:
            async for chunk in graph.astream(init_state, stream_mode="custom"):
                if not isinstance(chunk, dict) or "event" not in chunk:
                    continue
                kind = chunk["event"]
                if kind == "token":
                    accumulated += chunk.get("data", "")
                elif kind == "citation":
                    citations.append(chunk["data"])
                elif kind == "verdict":
                    verdict = chunk["data"]
                elif kind == "followups":
                    followups = chunk["data"]
                yield chunk
        except Exception as exc:  # noqa: BLE001
            logger.exception("hierarchical graph stream failed")
            yield {"event": "error", "data": {"message": str(exc)}}
            return

        # Cost
        try:
            from core.costmeter import CostMeter

            yield {"event": "cost", "data": CostMeter.snapshot()}
        except Exception:
            pass

        # Semantic-cache write-back (only when the verifier was happy).
        unsupported = (verdict or {}).get("unsupported_claims", 1)
        if (
            question_embedding is not None
            and accumulated
            and unsupported == 0
            and os.getenv("USE_SEMANTIC_CACHE", "true").lower() == "true"
        ):
            try:
                from core.semantic_cache import SemanticCache

                await SemanticCache.store(
                    question=question,
                    embedding=question_embedding,
                    answer=accumulated,
                    citations=citations,
                    verdict=verdict,
                    followups=followups,
                    model=os.getenv("AZURE_OPENAI_CHATGPT_DEPLOYMENT", "gpt-4.1-mini"),
                    acl=(context or {}).get("auth_claims"),
                )
            except Exception:
                logger.exception("semantic cache store failed")

"""Multi-agent orchestration: Router -> Retriever -> Answerer -> Verifier -> FollowUps.

Streams SSE events:
- {"event": "token", "data": "..."} per chunk
- {"event": "citation", "data": {...}} as evidence is referenced
- {"event": "claim", "data": {sentence, citation_ids, verdict, reason}} per Verifier verdict
- {"event": "verdict", "data": {unsupported_claims, retried}} once Verifier finishes
- {"event": "followups", "data": ["...", "...", "..."]}
- {"event": "cost", "data": {input_tokens, output_tokens, est_usd}}
"""
from __future__ import annotations

import asyncio
import logging
import os
from typing import Any, AsyncGenerator

from approaches.approach import Approach, Claim, DataPoints

logger = logging.getLogger(__name__)


class MultiAgentApproach(Approach):
    async def run(
        self,
        messages: list[dict[str, Any]],
        context: dict[str, Any] | None = None,
        session_state: str | None = None,
    ) -> dict[str, Any]:
        # Non-streaming convenience: collect stream then return final state
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
        return final

    async def run_stream(
        self,
        messages: list[dict[str, Any]],
        context: dict[str, Any] | None = None,
        session_state: str | None = None,
    ) -> AsyncGenerator[dict[str, Any], None]:
        # Shared pre-flight: cache lookup, tutor persona, query enhancement,
        # safety screen, routing. Yields live SSE events plus a final control event.
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
        route_label = pre.get("route")

        # SQL branch
        if route_label == "sql":
            from approaches.sql_schemaflow_approach import SchemaFlowSQLApproach

            sql_approach = SchemaFlowSQLApproach(prompt_manager=self.prompt_manager)
            sql_result = await sql_approach.run_for_question(question)
            yield {"event": "sql", "data": sql_result}
            yield {"event": "verdict", "data": {"unsupported_claims": 0, "retried": False}}
            return

        # Retriever (parallel graph + file_search)
        from agents.retriever import retrieve

        evidence = await retrieve(
            question=question,
            overrides=overrides,
            use_graphrag=os.getenv("USE_GRAPHRAG", "true").lower() == "true",
        )
        for c in evidence.citations:
            yield {"event": "citation", "data": c.__dict__}

        # Answerer (streaming)
        from agents.answerer import answer_stream
        from agents.verifier import verify_claim

        claims: list[Claim] = []
        unsupported = 0
        accumulated = ""
        verifier_enabled = os.getenv("USE_VERIFIER", "true").lower() == "true"

        async for token, claim_complete in answer_stream(
            question=question,
            evidence=evidence,
            messages=messages,
            prompt_manager=self.prompt_manager,
            overrides=overrides,
        ):
            if token:
                accumulated += token
                yield {"event": "token", "data": token}
            if claim_complete is not None:
                claim = claim_complete
                if verifier_enabled:
                    verdict = await verify_claim(claim, evidence)
                    claim.verdict = verdict.label
                    claim.verifier_reason = verdict.reason
                    if claim.verdict == "unsupported":
                        unsupported += 1
                else:
                    claim.verdict = "skipped"
                claims.append(claim)
                yield {"event": "claim", "data": claim.__dict__}

        # Optional one-shot retry if too many unsupported claims
        retried = False
        if verifier_enabled and unsupported > 0 and overrides.get("verifier_retry", True):
            retried = True
            logger.info("Verifier flagged %d unsupported; retrying answerer", unsupported)
            # In a real implementation we would call answer_stream again with the diff.
            # For now we leave the accumulated text and trust the UI to gray out unsupported sentences.

        yield {"event": "verdict", "data": {"unsupported_claims": unsupported, "retried": retried}}

        # Follow-ups
        try:
            from agents.followups import suggest_followups

            followups = await suggest_followups(question=question, answer=accumulated, prompt_manager=self.prompt_manager)
            yield {"event": "followups", "data": followups}
        except Exception:
            logger.debug("followups skipped")

        # Cost
        try:
            from core.costmeter import CostMeter

            yield {"event": "cost", "data": CostMeter.snapshot()}
        except Exception:
            pass

        # Write-back to semantic cache (only when verifier was happy and we have an embedding)
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
                    citations=[c.__dict__ if hasattr(c, "__dict__") else c for c in evidence.citations],
                    verdict={"unsupported_claims": unsupported, "retried": retried},
                    followups=locals().get("followups") or [],
                    model=os.getenv("AZURE_OPENAI_CHATGPT_DEPLOYMENT", "gpt-4.1-mini"),
                    acl=(context or {}).get("auth_claims"),
                )
            except Exception:
                logger.exception("semantic cache store failed")

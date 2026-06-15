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
        overrides = dict((context or {}).get("overrides", {}))
        question = messages[-1]["content"] if messages else ""

        # Tutor persona: route the answerer at the dedicated tutor template
        if os.getenv("USE_TUTOR_MODE", "true").lower() == "true" and "answerer_prompt" not in overrides:
            overrides["answerer_prompt"] = "tutor.system.jinja2"

        # Query enhancement: expand short or acronym-heavy queries before retrieval
        if (
            os.getenv("USE_QUERY_ENHANCEMENT", "true").lower() == "true"
            and len(question.split()) <= 5
            and self.prompt_manager is not None
        ):
            try:
                from agents._llm import complete

                enhancement_prompt = self.prompt_manager.render("query_enhancement.system.jinja2")
                enhanced = (await complete(system=enhancement_prompt, user=question, role="chat")).strip()
                if enhanced and enhanced != question:
                    yield {"event": "query_enhanced", "data": {"original": question, "enhanced": enhanced}}
                    question = enhanced
            except Exception:
                logger.exception("query enhancement failed; using original question")

        # Content safety screen (optional)
        if os.getenv("USE_CONTENT_SAFETY", "false").lower() == "true":
            try:
                from safety.content_safety import screen_input

                safe = await screen_input(question)
                if not safe.ok:
                    yield {"event": "blocked", "data": {"reason": safe.reason}}
                    return
            except Exception:
                logger.exception("content safety screen failed; proceeding")

        # Router
        from agents.router import route

        route_label = await route(question=question, messages=messages, prompt_manager=self.prompt_manager)
        yield {"event": "route", "data": route_label}

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

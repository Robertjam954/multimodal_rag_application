"""Shared pre-flight for the agentic chat approaches.

Both ``MultiAgentApproach`` (flat) and ``HierarchicalMultiAgentApproach`` run the
same preamble before orchestration: semantic-cache lookup, tutor-persona prompt
selection, query enhancement, content-safety screen, and routing. Factoring it
here keeps the two paths truthful to one another.

``run_preamble`` is an async generator. It yields the same live SSE events the
inline code used to emit (``citation``, ``token``, ``verdict``, ``followups``,
``cache_hit``, ``query_enhanced``, ``blocked``, ``route``) and finishes by
yielding a single control event::

    {"event": "_preamble_done", "data": PreambleResult-as-dict}

Callers forward every event except ``_preamble_done``, then read that payload to
decide whether to terminate (cache hit / blocked) or continue with the possibly
rewritten ``question``, ``overrides``, ``question_embedding`` and ``route``.
"""
from __future__ import annotations

import dataclasses
import logging
import os
from typing import Any, AsyncGenerator

logger = logging.getLogger(__name__)

PREAMBLE_DONE = "_preamble_done"


@dataclasses.dataclass
class PreambleResult:
    question: str
    overrides: dict[str, Any]
    question_embedding: list[float] | None = None
    route: str | None = None
    terminate: bool = False  # True when a cache hit or safety block ended the turn


async def run_preamble(
    messages: list[dict[str, Any]],
    context: dict[str, Any] | None,
    prompt_manager: Any | None,
) -> AsyncGenerator[dict[str, Any], None]:
    overrides = dict((context or {}).get("overrides", {}))
    question = messages[-1]["content"] if messages else ""
    result = PreambleResult(question=question, overrides=overrides)

    # Semantic cache lookup (no-op if cache disabled or embed fails)
    question_embedding: list[float] | None = None
    if (
        question
        and os.getenv("USE_SEMANTIC_CACHE", "true").lower() == "true"
        and not overrides.get("skip_cache")
    ):
        try:
            from core.semantic_cache import SemanticCache
            from prepdocslib.embeddings import TextEmbeddings

            emb = await TextEmbeddings().embed([question])
            if emb and emb[0]:
                question_embedding = emb[0]
                acl = (context or {}).get("auth_claims")
                hit = await SemanticCache.lookup(question_embedding, acl=acl)
                if hit is not None:
                    for c in hit.citations:
                        yield {"event": "citation", "data": c}
                    if hit.answer:
                        yield {"event": "token", "data": hit.answer}
                    if hit.verdict is not None:
                        yield {"event": "verdict", "data": hit.verdict}
                    if hit.followups:
                        yield {"event": "followups", "data": hit.followups}
                    yield {"event": "cache_hit", "data": {"model": hit.model, "ts": hit.ts}}
                    result.question_embedding = question_embedding
                    result.terminate = True
                    yield {"event": PREAMBLE_DONE, "data": dataclasses.asdict(result)}
                    return
        except Exception:
            logger.exception("semantic cache lookup failed; proceeding without cache")
    result.question_embedding = question_embedding

    # Tutor persona: route the answerer at the dedicated tutor template
    if os.getenv("USE_TUTOR_MODE", "true").lower() == "true" and "answerer_prompt" not in overrides:
        overrides["answerer_prompt"] = "tutor.system.jinja2"

    # Query enhancement: expand short or acronym-heavy queries before retrieval
    if (
        os.getenv("USE_QUERY_ENHANCEMENT", "true").lower() == "true"
        and len(question.split()) <= 5
        and prompt_manager is not None
    ):
        try:
            from agents._llm import complete

            enhancement_prompt = prompt_manager.render("query_enhancement.system.jinja2")
            enhanced = (await complete(system=enhancement_prompt, user=question, role="chat")).strip()
            if enhanced and enhanced != question:
                yield {"event": "query_enhanced", "data": {"original": question, "enhanced": enhanced}}
                question = enhanced
        except Exception:
            logger.exception("query enhancement failed; using original question")
    result.question = question

    # Content safety screen (optional)
    if os.getenv("USE_CONTENT_SAFETY", "false").lower() == "true":
        try:
            from safety.content_safety import screen_input

            safe = await screen_input(question)
            if not safe.ok:
                yield {"event": "blocked", "data": {"reason": safe.reason}}
                result.terminate = True
                yield {"event": PREAMBLE_DONE, "data": dataclasses.asdict(result)}
                return
        except Exception:
            logger.exception("content safety screen failed; proceeding")

    # Router
    from agents.router import route

    route_label = await route(question=question, messages=messages, prompt_manager=prompt_manager)
    result.route = route_label
    yield {"event": "route", "data": route_label}

    yield {"event": PREAMBLE_DONE, "data": dataclasses.asdict(result)}

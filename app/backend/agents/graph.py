"""LangGraph wiring for the multi-agent loop.

In production this replaces the inline orchestration inside MultiAgentApproach.run_stream.
Kept here as a clean reference graph for future migration; not used at runtime today.
"""
from __future__ import annotations

import logging
from typing import Any, TypedDict

logger = logging.getLogger(__name__)


class GraphState(TypedDict, total=False):
    question: str
    messages: list[dict[str, Any]]
    route: str
    evidence: Any
    answer: str
    claims: list[Any]
    verdict: dict[str, Any]
    followups: list[str]


def build_graph():
    """Construct a LangGraph StateGraph. Returns the compiled graph or None if langgraph is absent."""
    try:
        from langgraph.graph import END, StateGraph
    except Exception:
        logger.info("langgraph not installed; build_graph returning None")
        return None

    from agents.answerer import answer as answer_node
    from agents.followups import suggest_followups
    from agents.retriever import retrieve as retriever_node
    from agents.router import route as router_node
    from agents.verifier import verify_claim
    from approaches.approach import DataPoints

    async def _route(state: GraphState) -> GraphState:
        state["route"] = await router_node(state["question"], state.get("messages") or [])
        return state

    async def _retrieve(state: GraphState) -> GraphState:
        state["evidence"] = await retriever_node(state["question"])
        return state

    async def _answer(state: GraphState) -> GraphState:
        text, claims, _ = await answer_node(
            question=state["question"],
            evidence=state["evidence"],
            messages=state.get("messages") or [],
            prompt_manager=None,
        )
        state["answer"] = text
        state["claims"] = claims
        return state

    async def _verify(state: GraphState) -> GraphState:
        evidence: DataPoints = state["evidence"]
        unsupported = 0
        for c in state["claims"]:
            v = await verify_claim(c, evidence)
            c.verdict = v.label
            c.verifier_reason = v.reason
            if v.label == "unsupported":
                unsupported += 1
        state["verdict"] = {"unsupported_claims": unsupported, "retried": False}
        return state

    async def _followups(state: GraphState) -> GraphState:
        state["followups"] = await suggest_followups(state["question"], state["answer"])
        return state

    g = StateGraph(GraphState)
    g.add_node("route", _route)
    g.add_node("retrieve", _retrieve)
    g.add_node("answer", _answer)
    g.add_node("verify", _verify)
    g.add_node("followups", _followups)
    g.set_entry_point("route")
    g.add_edge("route", "retrieve")
    g.add_edge("retrieve", "answer")
    g.add_edge("answer", "verify")
    g.add_edge("verify", "followups")
    g.add_edge("followups", END)
    return g.compile()

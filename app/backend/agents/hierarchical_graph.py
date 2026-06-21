"""Hierarchical agent teams (opt-in, LangGraph).

Adapts the LangGraph "Hierarchical Agent Teams" pattern to this app. A top-level
coordinator divides work between three teams:

    top coordinator
    ├── retrieval_team   - LLM supervisor over Azure-skill workers
    │     ├── file_searcher   (file_search + azure_ai_search skills)
    │     ├── graph_searcher  (graph_search skill)
    │     └── notes_searcher  (notes_search + get_document skills)
    ├── answer_team      - deterministic answer -> verify -> followups pipeline
    └── sql_team         - SchemaFlow Parse/Impact/Plan/SQL

Design choices:
- The **retrieval team** is a genuine LLM-supervised sub-team (``make_supervisor_node``)
  whose workers are ``create_react_agent`` instances with Azure skills bound -
  this is where "Azure skills for every agent" lives.
- The **top coordinator** is a deterministic state-machine (reliable production
  path) rather than an LLM coin-flip: it routes sql -> sql_team, else
  retrieval_team -> answer_team -> END.
- The **answer team** reuses the existing streaming answerer + per-claim verifier
  so token streaming and the Verifier gate keep full fidelity.

Nodes stream SSE-shaped events through a LangGraph custom ``StreamWriter`` so the
``HierarchicalMultiAgentApproach`` can forward the exact same event schema as the
flat ``MultiAgentApproach`` (token / citation / claim / verdict / followups / sql).

``build_hierarchical_graph`` returns the compiled graph, or ``None`` when
LangGraph / a LLM provider is unavailable (caller then falls back to flat).
"""
from __future__ import annotations

import json
import logging
import os
from typing import Any

logger = logging.getLogger(__name__)


def _collate_evidence(messages: list[Any]):
    """Build DataPoints from the retrieval team's tool outputs (our skills' JSON)."""
    from approaches.approach import Citation, DataPoints

    citations: list[Citation] = []
    text_snippets: list[str] = []
    subgraph: dict[str, Any] | None = None

    try:
        from langchain_core.messages import ToolMessage
    except Exception:
        ToolMessage = tuple()  # type: ignore

    for m in messages:
        if not isinstance(m, ToolMessage):
            continue
        try:
            payload = json.loads(m.content)
        except Exception:
            continue
        # list of hits (file_search / azure_ai_search)
        if isinstance(payload, list):
            for r in payload:
                if not isinstance(r, dict):
                    continue
                cid = r.get("id") or r.get("filename") or r.get("source_file") or "?"
                citations.append(
                    Citation(
                        id=str(cid),
                        source_file=r.get("filename") or r.get("source_file") or "unknown",
                        source_page=str(r.get("page")) if r.get("page") else None,
                        score=r.get("score"),
                        content_snippet=(r.get("content") or "")[:1500],
                    )
                )
                text_snippets.append(r.get("content") or "")
        # graph_search dict
        elif isinstance(payload, dict):
            if "nodes" in payload or "community_chunks" in payload:
                subgraph = {"nodes": payload.get("nodes", []), "edges": payload.get("edges", [])}
                for chunk in payload.get("community_chunks", []):
                    citations.append(
                        Citation(
                            id=str(chunk.get("id", "community")),
                            source_file=chunk.get("source", "graphrag-community"),
                            content_snippet=(chunk.get("text") or "")[:1500],
                        )
                    )
                    text_snippets.append(chunk.get("text") or "")
            # notes_search dict with hits
            for hit in payload.get("hits", []) if isinstance(payload, dict) else []:
                if not isinstance(hit, dict):
                    continue
                cid = hit.get("id") or hit.get("note_id") or "note"
                citations.append(
                    Citation(
                        id=str(cid),
                        source_file=hit.get("source_url") or hit.get("content_topic") or "note",
                        content_snippet=(hit.get("content") or hit.get("snippet") or "")[:1500],
                    )
                )
                text_snippets.append(hit.get("content") or hit.get("snippet") or "")

    return DataPoints(text=text_snippets, citations=citations, graph_subgraph=subgraph)


def make_supervisor_node(llm, members: list[str]):
    """LLM router over `members`; routes to a member or FINISH. Adapted from the
    LangGraph hierarchical-teams notebook."""
    from langgraph.graph import END
    from langgraph.types import Command
    from typing_extensions import TypedDict

    options = ["FINISH"] + members
    system_prompt = (
        "You are a supervisor managing these workers: "
        f"{members}. Given the conversation, respond with the worker to act next. "
        "Each worker performs a task and reports back. When the user's request is "
        "fully answered, respond with FINISH."
    )

    class Router(TypedDict):
        next: str  # one of options

    def supervisor_node(state) -> Command:
        messages = [{"role": "system", "content": system_prompt}] + state["messages"]
        try:
            response = llm.with_structured_output(Router).invoke(messages)
            goto = response["next"]
        except Exception:
            logger.exception("supervisor routing failed; finishing")
            goto = "FINISH"
        if goto not in options:
            goto = "FINISH"
        if goto == "FINISH":
            goto = END
        return Command(goto=goto, update={"next": goto})

    return supervisor_node


def _build_retrieval_subgraph(llm, prompt_manager=None):
    """Retrieval team: supervisor + Azure-skill react workers."""
    from langchain_core.messages import HumanMessage
    from langgraph.graph import START, StateGraph, MessagesState
    from langgraph.prebuilt import create_react_agent
    from langgraph.types import Command

    from agents.skills import (
        azure_ai_search_skill,
        file_search_skill,
        get_document_skill,
        graph_search_skill,
        notes_search_skill,
    )

    file_agent = create_react_agent(llm, tools=[file_search_skill, azure_ai_search_skill])
    graph_agent = create_react_agent(llm, tools=[graph_search_skill])
    notes_agent = create_react_agent(llm, tools=[notes_search_skill, get_document_skill])

    def _worker(agent, name):
        def node(state) -> Command:
            result = agent.invoke(state)
            return Command(
                update={"messages": [HumanMessage(content=result["messages"][-1].content, name=name)]},
                goto="supervisor",
            )

        return node

    supervisor = make_supervisor_node(llm, ["file_searcher", "graph_searcher", "notes_searcher"])

    builder = StateGraph(MessagesState)
    builder.add_node("supervisor", supervisor)
    builder.add_node("file_searcher", _worker(file_agent, "file_searcher"))
    builder.add_node("graph_searcher", _worker(graph_agent, "graph_searcher"))
    builder.add_node("notes_searcher", _worker(notes_agent, "notes_searcher"))
    builder.add_edge(START, "supervisor")
    return builder.compile()


def build_hierarchical_graph(prompt_manager=None):
    """Compile the top-level hierarchical graph, or return None if unavailable."""
    try:
        from langchain_core.messages import HumanMessage
        from langgraph.graph import END, START, StateGraph, MessagesState
        from langgraph.types import Command, StreamWriter

        from agents._chat_model import chat_model
        from approaches.approach import Claim, DataPoints
    except Exception:
        logger.info("langgraph / langchain unavailable; build_hierarchical_graph returning None")
        return None

    llm = chat_model(role="chat")
    if llm is None:
        logger.info("no LLM provider configured; build_hierarchical_graph returning None")
        return None

    reasoning_llm = chat_model(role="reasoning") or llm
    retrieval_subgraph = _build_retrieval_subgraph(llm, prompt_manager)
    verifier_enabled = os.getenv("USE_VERIFIER", "true").lower() == "true"

    class State(MessagesState):
        question: str
        overrides: dict
        route: str
        evidence: Any
        answer: str
        claims: list
        verdict: dict
        followups: list

    # ---- top coordinator (deterministic) ----
    def coordinator(state: State) -> Command:
        route = state.get("route")
        if route == "sql" and "verdict" not in state:
            return Command(goto="sql_team")
        if "evidence" not in state:
            return Command(goto="retrieval_team")
        if "answer" not in state:
            return Command(goto="answer_team")
        return Command(goto=END)

    # ---- retrieval team node ----
    def retrieval_team(state: State, writer: StreamWriter) -> Command:
        question = state["question"]
        evidence = None
        try:
            sub = retrieval_subgraph.invoke({"messages": [HumanMessage(content=question)]})
            evidence = _collate_evidence(sub.get("messages", []))
        except Exception:
            logger.exception("retrieval team failed; falling back to deterministic retrieve")
        if evidence is None or not evidence.citations:
            from agents.retriever import retrieve

            evidence = _run_sync(
                retrieve(
                    question=question,
                    overrides=state.get("overrides", {}),
                    use_graphrag=os.getenv("USE_GRAPHRAG", "true").lower() == "true",
                )
            )
        for c in evidence.citations:
            writer({"event": "citation", "data": c.__dict__})
        return Command(goto="coordinator", update={"evidence": evidence})

    # ---- answer team node (answer -> verify -> followups) ----
    def answer_team(state: State, writer: StreamWriter) -> Command:
        from agents.answerer import answer_stream
        from agents.followups import suggest_followups
        from agents.verifier import verify_claim

        question = state["question"]
        evidence: DataPoints = state["evidence"]
        overrides = state.get("overrides", {})

        claims: list[Claim] = []
        unsupported = 0
        accumulated = ""

        async def _drive() -> None:
            nonlocal accumulated, unsupported
            async for token, claim_complete in answer_stream(
                question=question,
                evidence=evidence,
                messages=state.get("messages_raw", []),
                prompt_manager=prompt_manager,
                overrides=overrides,
            ):
                if token:
                    accumulated += token
                    writer({"event": "token", "data": token})
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
                    writer({"event": "claim", "data": claim.__dict__})

        _run_sync(_drive())
        writer({"event": "verdict", "data": {"unsupported_claims": unsupported, "retried": False}})

        followups: list[str] = []
        try:
            followups = _run_sync(suggest_followups(question=question, answer=accumulated, prompt_manager=prompt_manager))
            writer({"event": "followups", "data": followups})
        except Exception:
            logger.debug("followups skipped")

        return Command(
            goto="coordinator",
            update={
                "answer": accumulated,
                "claims": [c.__dict__ for c in claims],
                "verdict": {"unsupported_claims": unsupported, "retried": False},
                "followups": followups,
            },
        )

    # ---- sql team node ----
    def sql_team(state: State, writer: StreamWriter) -> Command:
        from approaches.sql_schemaflow_approach import SchemaFlowSQLApproach

        result = _run_sync(SchemaFlowSQLApproach(prompt_manager=prompt_manager).run_for_question(state["question"]))
        writer({"event": "sql", "data": result})
        writer({"event": "verdict", "data": {"unsupported_claims": 0, "retried": False}})
        return Command(goto="coordinator", update={"verdict": {"unsupported_claims": 0, "retried": False}})

    builder = StateGraph(State)
    builder.add_node("coordinator", coordinator)
    builder.add_node("retrieval_team", retrieval_team)
    builder.add_node("answer_team", answer_team)
    builder.add_node("sql_team", sql_team)
    builder.add_edge(START, "coordinator")
    return builder.compile()


def _run_sync(coro):
    """Run a coroutine to completion from within a sync LangGraph node.

    LangGraph invokes our nodes synchronously here; the wrapped agent functions
    are async. Use a private event loop in a worker thread to avoid clashing with
    any already-running loop on the calling thread.
    """
    import asyncio

    try:
        asyncio.get_running_loop()
    except RuntimeError:
        return asyncio.run(coro)

    # A loop is already running on this thread: run the coroutine in a fresh loop
    # on a separate thread and block for the result.
    import concurrent.futures

    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as pool:
        return pool.submit(lambda: asyncio.run(coro)).result()

"""Chainlit frontend for the AI Engineering Tutor.

Wires Chainlit's chat UI directly to:
- `core.aoai_client.get_client` (Grok-4 on Foundry via AAD)
- `core.document_retriever.get_retriever` for both `search_notes` and `get_document` tools
- `core.conversation_memory.ConversationMemory` for cross-session persistence

After every agent answer this renders a "Sources" block listing:
  * the document name (content_topic)
  * the exact chunk that was retrieved
  * a "View full document" action button (calls get_document)

Run with:
    cd app/backend
    chainlit run chainlit_app.py --host 0.0.0.0 --port 8000
"""
from __future__ import annotations

import json
import logging
import re
import uuid
from typing import Any

import chainlit as cl
from dotenv import load_dotenv

load_dotenv()

from agents.notes_search_tool import (
    GET_DOCUMENT_SCHEMA,
    SEARCH_NOTES_SCHEMA,
    get_document,
    search_notes,
)
from agents.tutor_agent import MAX_TOOL_HOPS, SYSTEM_PROMPT
from core.aoai_client import chat_deployment, get_client
from core.conversation_memory import ConversationMemory, UserFacts, messages_for_llm

logger = logging.getLogger(__name__)

_TOOL_REGISTRY = {"search_notes": search_notes, "get_document": get_document}
_TOOLS = [SEARCH_NOTES_SCHEMA, GET_DOCUMENT_SCHEMA]

NOTE_REF_RE = re.compile(r"\[note:([A-Za-z0-9_-]+)\]")


def _session_id() -> str:
    return cl.user_session.get("session_id") or "unknown"


async def _execute_tool(name: str, arguments_raw: str) -> str:
    fn = _TOOL_REGISTRY.get(name)
    if fn is None:
        return json.dumps({"error": f"unknown_tool:{name}"})
    try:
        args = json.loads(arguments_raw or "{}")
    except json.JSONDecodeError:
        return json.dumps({"error": "bad_arguments_json", "raw": arguments_raw})
    try:
        result = await fn(**args)
    except TypeError as exc:
        return json.dumps({"error": "bad_arguments", "detail": str(exc)})
    except Exception as exc:  # noqa: BLE001
        logger.exception("tool %s failed", name)
        return json.dumps({"error": "tool_exception", "detail": str(exc)})
    return json.dumps(result, default=str)


def _record_search_hits(turn_hits: dict[str, dict[str, Any]], tool_name: str, output_raw: str) -> None:
    """Pluck hits out of a search_notes tool output and store the best chunk per note_id."""
    if tool_name != "search_notes":
        return
    try:
        payload = json.loads(output_raw)
    except json.JSONDecodeError:
        return
    for hit in payload.get("hits", []) or []:
        note_id = hit.get("note_id")
        if not note_id:
            continue
        existing = turn_hits.get(note_id)
        # Keep the highest-similarity chunk per note_id
        if existing is None or hit.get("similarity", 0) > existing.get("similarity", 0):
            turn_hits[note_id] = hit


def _cited_note_ids(answer: str) -> list[str]:
    seen: list[str] = []
    for m in NOTE_REF_RE.finditer(answer):
        nid = m.group(1)
        if nid not in seen:
            seen.append(nid)
    return seen


async def _render_sources(
    cited_ids: list[str],
    turn_hits: dict[str, dict[str, Any]],
) -> None:
    """Send a Sources block: one source per cited note_id with chunk + name + view button."""
    if not cited_ids:
        return

    # Build a markdown body with all sources at once; attach a View action per source.
    lines = ["### Sources"]
    actions: list[cl.Action] = []

    for i, note_id in enumerate(cited_ids, 1):
        hit = turn_hits.get(note_id)
        if hit is None:
            # Citation refers to a note not in this turn's search results - fetch it cold.
            try:
                doc = await get_document(note_id)
            except Exception:  # noqa: BLE001
                doc = {}
            content_topic = doc.get("content_topic") or "(unknown document)"
            source_url = doc.get("source_url") or ""
            chunk_excerpt = (doc.get("content") or "").strip()[:400]
            similarity_str = ""
        else:
            content_topic = hit.get("content_topic") or "(untitled)"
            source_url = hit.get("source_url") or ""
            chunk_excerpt = (hit.get("content") or "").strip()[:400]
            sim = hit.get("similarity")
            similarity_str = f"  _similarity {sim:.3f}_" if isinstance(sim, (int, float)) else ""

        title_line = f"**{i}. {content_topic}**{similarity_str}"
        if source_url:
            title_line += f"  \n[{source_url}]({source_url})"
        lines.append(title_line)
        lines.append(f"> {chunk_excerpt}")
        lines.append(f"`note_id: {note_id}`")
        lines.append("")

        actions.append(
            cl.Action(
                name="view_document",
                payload={"note_id": note_id, "content_topic": content_topic},
                label=f"View source {i}",
                description=f"Show the full document for {content_topic[:60]}",
            )
        )

    await cl.Message(content="\n".join(lines), author="Sources", actions=actions).send()


@cl.on_chat_start
async def on_chat_start() -> None:
    sid = f"chainlit-{uuid.uuid4().hex[:12]}"
    cl.user_session.set("session_id", sid)

    welcome = (
        "Hey - I'm an AI engineering tutor. Ask me about topics in your notes "
        "library (RAG, prompt caching, retrieval, verifiers, GraphRAG, NL-to-SQL, "
        "YouTube ingestion) and I'll cite the source notes inline. Every answer "
        "is followed by a Sources block showing the exact chunk + document name. "
        "Click **View source N** to see the full document.\n\n"
        f"Session: `{sid}` (turns persist 30 days)."
    )
    await cl.Message(content=welcome, author="Tutor").send()


@cl.on_message
async def on_message(message: cl.Message) -> None:
    sid = _session_id()
    user_text = message.content.strip()
    if not user_text:
        return

    history_turns = await ConversationMemory.recall(sid, k=20)
    facts = await UserFacts.all(sid)

    messages: list[dict[str, Any]] = [{"role": "system", "content": SYSTEM_PROMPT}]
    messages.extend(messages_for_llm(history_turns, facts=facts))
    messages.append({"role": "user", "content": user_text})

    client = get_client()
    model = chat_deployment()

    answer_msg = cl.Message(content="", author="Tutor")
    await answer_msg.send()

    # Track every chunk this turn's search_notes calls returned, keyed by note_id.
    turn_hits: dict[str, dict[str, Any]] = {}
    final_answer = ""

    for hop in range(MAX_TOOL_HOPS):
        try:
            stream = await client.chat.completions.create(
                model=model,
                messages=messages,
                tools=_TOOLS,
                tool_choice="auto",
                stream=True,
            )
        except Exception as exc:  # noqa: BLE001
            logger.exception("Grok call failed")
            await cl.Message(content=f"LLM error: {exc}", author="System").send()
            return

        content_buf = ""
        tool_calls: dict[int, dict[str, str]] = {}

        async for chunk in stream:
            if not chunk.choices:
                continue
            delta = chunk.choices[0].delta
            if delta.content:
                content_buf += delta.content
                await answer_msg.stream_token(delta.content)
            if delta.tool_calls:
                for tc in delta.tool_calls:
                    idx = tc.index
                    slot = tool_calls.setdefault(idx, {"id": "", "name": "", "arguments": ""})
                    if tc.id:
                        slot["id"] = tc.id
                    if tc.function:
                        if tc.function.name:
                            slot["name"] = tc.function.name
                        if tc.function.arguments:
                            slot["arguments"] += tc.function.arguments

        if not tool_calls:
            final_answer = content_buf
            break

        messages.append(
            {
                "role": "assistant",
                "content": content_buf or None,
                "tool_calls": [
                    {
                        "id": slot["id"] or f"call_{idx}",
                        "type": "function",
                        "function": {"name": slot["name"], "arguments": slot["arguments"]},
                    }
                    for idx, slot in sorted(tool_calls.items())
                ],
            }
        )

        for idx, slot in sorted(tool_calls.items()):
            tool_name = slot["name"]
            args = slot["arguments"]
            async with cl.Step(name=tool_name, type="tool") as step:
                step.input = args
                output = await _execute_tool(tool_name, args)
                step.output = output[:4000]
            _record_search_hits(turn_hits, tool_name, output)
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": slot["id"] or f"call_{idx}",
                    "content": output,
                }
            )
    else:
        final_answer = (
            content_buf
            or "I couldn't converge within the tool budget. Try rephrasing the question."
        )

    await answer_msg.update()

    # Persist conversation
    await ConversationMemory.remember(sid, "user", user_text)
    if final_answer:
        await ConversationMemory.remember(sid, "assistant", final_answer)

    # Render the Sources block keyed off [note:<id>] citations in the final answer.
    cited_ids = _cited_note_ids(final_answer)
    await _render_sources(cited_ids, turn_hits)


@cl.action_callback("view_document")
async def on_view_document(action: cl.Action) -> None:
    payload = action.payload or {}
    note_id = payload.get("note_id")
    content_topic = payload.get("content_topic") or note_id or "(unknown)"
    if not note_id:
        await cl.Message(content="No note_id attached to that action.", author="System").send()
        return

    waiting = cl.Message(content=f"Fetching full document `{note_id}`...", author="System")
    await waiting.send()

    result = await get_document(note_id)
    if result.get("error"):
        waiting.content = f"Could not fetch `{note_id}`: {result['error']}"
        await waiting.update()
        return

    body_lines = [
        f"# {result.get('content_topic') or content_topic}",
        "",
    ]
    if result.get("source_url"):
        body_lines.append(f"**Source:** [{result['source_url']}]({result['source_url']})")
    if result.get("source_type"):
        body_lines.append(f"**Type:** {result['source_type']}")
    if result.get("tags"):
        body_lines.append(f"**Tags:** {', '.join(result['tags'])}")
    body_lines.append(f"**Chunks:** {result.get('chunk_count', '?')}  •  `note_id: {note_id}`")
    body_lines.append("")
    body_lines.append("---")
    body_lines.append("")
    body_lines.append(result.get("content", "(no content)"))

    waiting.content = "\n".join(body_lines)
    await waiting.update()

"""Tutor chat agent.

One turn:
1. Recall recent conversation history from Redis (ConversationMemory).
2. Build the message list: tutor system prompt + history + new user message.
3. Call the chat model (Grok-4 on Foundry via AAD) with `search_notes` tool exposed.
4. While the model responds with tool_calls, execute the tool and loop.
5. Persist both the user message and the final assistant message into memory.

Max tool hops capped to avoid runaway loops.
"""
from __future__ import annotations

import json
import logging
import time
from dataclasses import dataclass
from typing import Any

from agents.notes_search_tool import (
    GET_DOCUMENT_SCHEMA,
    SEARCH_NOTES_SCHEMA,
    get_document,
    search_notes,
)
from core.aoai_client import chat_deployment, get_client
from core.conversation_memory import ConversationMemory, UserFacts, messages_for_llm

logger = logging.getLogger(__name__)

MAX_TOOL_HOPS = 4

SYSTEM_PROMPT = (
    "You are an AI Engineering Tutor. You help the user move from 'I read about X' "
    "to 'I shipped X in production' through grounded, specific answers.\n\n"
    "Tooling:\n"
    "- You have a `search_notes` tool over an AI-engineering notes library. Call it "
    "  whenever the user asks about a topic the notes likely cover. Cite the matched "
    "  note inline as `[note:<note_id>]` the first time you reference it.\n"
    "- If the notes don't cover something, say so plainly. Do not invent facts, "
    "  version numbers, or pricing.\n\n"
    "Style:\n"
    "- Direct prose. No 'let's dive into' / 'in this article we will'.\n"
    "- Short code blocks only when the answer genuinely needs them (under ~30 lines).\n"
    "- For vague one- or two-word questions, ask one clarifying question instead of "
    "  guessing.\n"
    "- End with one 'What next' question the user could ask to deepen the topic."
)


@dataclass
class TurnResult:
    answer: str
    tool_calls: list[dict[str, Any]]
    duration_ms: int
    raw_messages: list[dict[str, Any]]


_TOOL_REGISTRY = {"search_notes": search_notes, "get_document": get_document}
_TOOLS = [SEARCH_NOTES_SCHEMA, GET_DOCUMENT_SCHEMA]


async def _dispatch_tool_call(tool_call: Any) -> str:
    name = tool_call.function.name
    args_raw = tool_call.function.arguments or "{}"
    try:
        args = json.loads(args_raw)
    except json.JSONDecodeError:
        return json.dumps({"error": "could_not_parse_arguments", "raw": args_raw})

    fn = _TOOL_REGISTRY.get(name)
    if fn is None:
        return json.dumps({"error": f"unknown_tool:{name}"})
    try:
        result = await fn(**args)
        return json.dumps(result, default=str)
    except TypeError as exc:
        return json.dumps({"error": "bad_arguments", "detail": str(exc)})
    except Exception as exc:  # noqa: BLE001
        logger.exception("tool %s failed", name)
        return json.dumps({"error": "tool_exception", "detail": str(exc)})


async def chat_turn(
    user_message: str,
    *,
    session_id: str | None = None,
    include_facts: bool = True,
) -> TurnResult:
    if not user_message.strip():
        raise ValueError("user_message is required")

    started = time.time()
    client = get_client()
    model = chat_deployment()

    history_turns = await ConversationMemory.recall(session_id, k=20) if session_id else []
    facts = await UserFacts.all(session_id) if session_id and include_facts else {}

    messages: list[dict[str, Any]] = [{"role": "system", "content": SYSTEM_PROMPT}]
    messages.extend(messages_for_llm(history_turns, facts=facts if include_facts else None))
    messages.append({"role": "user", "content": user_message})

    tool_calls_made: list[dict[str, Any]] = []

    for hop in range(MAX_TOOL_HOPS):
        response = await client.chat.completions.create(
            model=model,
            messages=messages,
            tools=_TOOLS,
            tool_choice="auto",
        )
        choice = response.choices[0]
        msg = choice.message

        if msg.tool_calls:
            messages.append(msg.model_dump(exclude_none=True))
            for tc in msg.tool_calls:
                tool_output = await _dispatch_tool_call(tc)
                tool_calls_made.append(
                    {
                        "hop": hop,
                        "tool": tc.function.name,
                        "arguments": tc.function.arguments,
                        "output_preview": tool_output[:300],
                    }
                )
                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tc.id,
                        "content": tool_output,
                    }
                )
            continue

        answer = msg.content or ""
        if session_id:
            await ConversationMemory.remember(session_id, "user", user_message)
            await ConversationMemory.remember(session_id, "assistant", answer)

        return TurnResult(
            answer=answer,
            tool_calls=tool_calls_made,
            duration_ms=int((time.time() - started) * 1000),
            raw_messages=messages,
        )

    answer = "I tried but couldn't converge on an answer within the tool-call budget. Please rephrase."
    if session_id:
        await ConversationMemory.remember(session_id, "user", user_message)
        await ConversationMemory.remember(session_id, "assistant", answer)
    return TurnResult(
        answer=answer,
        tool_calls=tool_calls_made,
        duration_ms=int((time.time() - started) * 1000),
        raw_messages=messages,
    )

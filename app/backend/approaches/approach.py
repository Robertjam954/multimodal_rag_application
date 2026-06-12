"""Base class for all approaches. Provides common types and helpers."""
from __future__ import annotations

import abc
import dataclasses
from typing import Any, AsyncGenerator


@dataclasses.dataclass
class Citation:
    id: str
    source_file: str
    source_page: str | None = None
    source_timestamp_seconds: float | None = None
    score: float | None = None
    content_snippet: str | None = None


@dataclasses.dataclass
class Claim:
    sentence: str
    citation_ids: list[str]
    verdict: str = "unknown"  # supported | unsupported | unknown
    verifier_reason: str | None = None


@dataclasses.dataclass
class DataPoints:
    """Container for retrieved evidence passed between Retriever, Answerer, Verifier."""
    text: list[str] = dataclasses.field(default_factory=list)
    images: list[dict[str, Any]] = dataclasses.field(default_factory=list)
    citations: list[Citation] = dataclasses.field(default_factory=list)
    graph_subgraph: dict[str, Any] | None = None
    annotations: list[dict[str, Any]] = dataclasses.field(default_factory=list)


@dataclasses.dataclass
class ThoughtStep:
    title: str
    description: str
    props: dict[str, Any] = dataclasses.field(default_factory=dict)


class Approach(abc.ABC):
    """Subclasses implement run() and (optionally) run_stream()."""

    def __init__(self, prompt_manager: Any | None = None) -> None:
        self.prompt_manager = prompt_manager

    @abc.abstractmethod
    async def run(
        self,
        messages: list[dict[str, Any]],
        context: dict[str, Any] | None = None,
        session_state: str | None = None,
    ) -> dict[str, Any]: ...

    async def run_stream(
        self,
        messages: list[dict[str, Any]],
        context: dict[str, Any] | None = None,
        session_state: str | None = None,
    ) -> AsyncGenerator[dict[str, Any], None]:
        """Default: yield the non-streaming result as a single event. Override for true streaming."""
        result = await self.run(messages, context, session_state)
        yield {"event": "answer", "data": result}

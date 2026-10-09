"""Local-only Vertex AI Reasoning Engine helpers for in-memory testing."""
from __future__ import annotations

import argparse
import os
from dataclasses import dataclass
from functools import lru_cache
from typing import Any, Callable, Sequence

DEFAULT_LOCATION = "us-central1"
DEFAULT_MODEL = "gemini-1.5-pro"
DEFAULT_PROMPT = "What was our Q3 revenue growth and how does it compare to the industry?"
DEFAULT_INSTRUCTIONS = "You are a local orchestrator. Route requests to appropriate tools."

ToolFn = Callable[[str], str]


@dataclass(frozen=True)
class LocalReasoningConfig:
    """Local execution settings for the Vertex AI reasoning engine demo."""

    project_id: str
    location: str = DEFAULT_LOCATION
    model: str = DEFAULT_MODEL
    instructions: str = DEFAULT_INSTRUCTIONS


def local_sql_tool(query: str) -> str:
    """Executes SQL against a local mock database."""
    print(f"\n[LOCAL EXECUTION] Executing SQL tool with query: {query}")
    return "Mock Result: {'revenue_q3': 1200000, 'growth': '12%'}"


def local_web_tool(query: str) -> str:
    """Simulates an external web lookup without leaving the local workflow."""
    print(f"\n[LOCAL EXECUTION] Executing Web tool with query: {query}")
    return "Mock Result: Industry average growth in Q3 was 8%."


def default_local_tools() -> tuple[ToolFn, ToolFn]:
    """Returns the default local mock toolset."""
    return (local_sql_tool, local_web_tool)


def resolve_local_config(
    project_id: str | None = None,
    location: str | None = None,
    model: str | None = None,
    instructions: str | None = None,
) -> LocalReasoningConfig:
    """Builds local execution config from explicit args and standard GCP env vars."""

    resolved_project_id = project_id or os.getenv("GOOGLE_CLOUD_PROJECT")
    if not resolved_project_id:
        raise ValueError("A GCP project ID is required. Pass --project-id or set GOOGLE_CLOUD_PROJECT.")

    return LocalReasoningConfig(
        project_id=resolved_project_id,
        location=location or os.getenv("GOOGLE_CLOUD_LOCATION", DEFAULT_LOCATION),
        model=model or DEFAULT_MODEL,
        instructions=instructions or DEFAULT_INSTRUCTIONS,
    )


def _load_vertex_modules() -> tuple[Any, Any]:
    try:
        import vertexai
        from vertexai.preview import reasoning_engines
    except ImportError as exc:
        raise RuntimeError(
            "google-cloud-aiplatform is required for local Vertex reasoning-engine runs. "
            "Sync app/backend/requirements.in before using this module."
        ) from exc

    return vertexai, reasoning_engines


def build_local_orchestrator(
    config: LocalReasoningConfig,
    tools: Sequence[ToolFn] | None = None,
) -> Any:
    """Instantiates the local LangchainAgent against Vertex AI Gemini."""

    vertexai, reasoning_engines = _load_vertex_modules()
    vertexai.init(project=config.project_id, location=config.location)

    return reasoning_engines.LangchainAgent(
        model=config.model,
        tools=list(tools or default_local_tools()),
        instructions=config.instructions,
    )


@lru_cache(maxsize=1)
def _cached_default_orchestrator(
    project_id: str,
    location: str,
    model: str,
    instructions: str,
) -> Any:
    return build_local_orchestrator(
        LocalReasoningConfig(
            project_id=project_id,
            location=location,
            model=model,
            instructions=instructions,
        )
    )


def clear_local_orchestrator_cache() -> None:
    """Clears the cached default orchestrator, mainly for tests."""
    _cached_default_orchestrator.cache_clear()


def get_local_orchestrator(
    config: LocalReasoningConfig | None = None,
    tools: Sequence[ToolFn] | None = None,
) -> Any:
    """Returns a local orchestrator instance, caching the default configuration."""

    resolved_config = config or resolve_local_config()
    if tools is not None:
        return build_local_orchestrator(resolved_config, tools=tools)

    return _cached_default_orchestrator(
        resolved_config.project_id,
        resolved_config.location,
        resolved_config.model,
        resolved_config.instructions,
    )


def query_local_orchestrator(
    prompt: str,
    *,
    config: LocalReasoningConfig | None = None,
    tools: Sequence[ToolFn] | None = None,
    orchestrator: Any | None = None,
) -> Any:
    """Executes a prompt through the local orchestrator."""

    if not prompt.strip():
        raise ValueError("Prompt is required for local reasoning-engine queries.")

    active_orchestrator = orchestrator or get_local_orchestrator(config=config, tools=tools)
    return active_orchestrator.query(input=prompt)


def _build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run the local Vertex AI reasoning-engine demo.")
    parser.add_argument("--project-id", help="GCP project ID. Defaults to GOOGLE_CLOUD_PROJECT.")
    parser.add_argument("--location", default=None, help=f"Vertex AI region. Defaults to {DEFAULT_LOCATION}.")
    parser.add_argument("--model", default=DEFAULT_MODEL, help=f"Gemini model name. Defaults to {DEFAULT_MODEL}.")
    parser.add_argument("--prompt", default=DEFAULT_PROMPT, help="Prompt to send to the local orchestrator.")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _build_arg_parser().parse_args(argv)
    config = resolve_local_config(project_id=args.project_id, location=args.location, model=args.model)

    print(f"User Prompt: {args.prompt}\n" + "-" * 50)
    response = query_local_orchestrator(args.prompt, config=config)
    print("\nFinal Orchestrator Response:")
    print(response)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

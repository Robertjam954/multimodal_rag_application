"""LangChain chat-model factory for the hierarchical agent teams.

``create_react_agent`` and ``make_supervisor_node`` need a LangChain
``BaseChatModel``. This mirrors the env routing in ``agents/_llm.py`` so the
hierarchical path uses the same Azure OpenAI / OpenAI / local-Ollama selection
and the same deployment names as the flat path.

Returns ``None`` when no provider is configured so callers can fall back cleanly.
"""
from __future__ import annotations

import logging
import os
from typing import Any

logger = logging.getLogger(__name__)


def _model_name(role: str) -> str:
    """Same deployment selection as agents/_llm.py:_model_for."""
    if os.getenv("MODE", "azure").lower() == "local":
        return os.getenv("OLLAMA_MODEL", "llama3.1:8b")
    if role == "reasoning":
        return os.getenv(
            "AZURE_OPENAI_REASONING_DEPLOYMENT",
            os.getenv("AZURE_OPENAI_CHATGPT_DEPLOYMENT", "gpt-4.1-mini"),
        )
    return os.getenv("AZURE_OPENAI_CHATGPT_DEPLOYMENT", os.getenv("OPENAI_CHATGPT_MODEL", "gpt-4.1-mini"))


def chat_model(role: str = "chat", **kwargs: Any):
    """Return a LangChain BaseChatModel configured for Azure / OpenAI / local.

    ``role`` selects the deployment ("chat" or "reasoning"). Returns ``None`` if
    no LLM provider env is set (keeps the hierarchical graph optional).
    """
    mode = os.getenv("MODE", "azure").lower()
    temperature = kwargs.pop("temperature", 0.2)

    try:
        if mode == "local":
            from langchain_openai import ChatOpenAI

            return ChatOpenAI(
                model=_model_name(role),
                base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1"),
                api_key=os.getenv("OLLAMA_API_KEY", "sk-local"),
                temperature=temperature,
                **kwargs,
            )

        if os.getenv("AZURE_OPENAI_SERVICE"):
            from langchain_openai import AzureChatOpenAI

            return AzureChatOpenAI(
                azure_endpoint=f"https://{os.getenv('AZURE_OPENAI_SERVICE')}.openai.azure.com/",
                azure_deployment=_model_name(role),
                api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-10-01-preview"),
                api_key=os.getenv("AZURE_OPENAI_API_KEY"),
                temperature=temperature,
                **kwargs,
            )

        if os.getenv("OPENAI_API_KEY"):
            from langchain_openai import ChatOpenAI

            return ChatOpenAI(
                model=_model_name(role),
                api_key=os.getenv("OPENAI_API_KEY"),
                temperature=temperature,
                **kwargs,
            )
    except Exception:
        logger.exception("chat_model construction failed; returning None")
        return None

    logger.info("chat_model: no LLM provider configured; returning None")
    return None

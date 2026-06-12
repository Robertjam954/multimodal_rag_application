"""Optional Azure AI Foundry Agent Service client.

When USE_FOUNDRY_HOSTED_AGENTS=true, calls a hosted agent instead of the in-process LangGraph.
Useful for multi-turn agents where latency tolerates server-side orchestration.
"""
from __future__ import annotations

import logging
import os
from typing import Any

logger = logging.getLogger(__name__)


class FoundryClient:
    def __init__(self, project_endpoint: str | None = None) -> None:
        self.project_endpoint = project_endpoint or os.getenv("AZURE_FOUNDRY_PROJECT_ENDPOINT")

    @property
    def enabled(self) -> bool:
        return os.getenv("USE_FOUNDRY_HOSTED_AGENTS", "false").lower() == "true" and bool(self.project_endpoint)

    async def run_agent(self, agent_id: str, input_text: str) -> dict[str, Any]:
        """Stub: real impl posts to Foundry Agent Service via azure-ai-projects SDK."""
        if not self.enabled:
            return {"output": f"[foundry-disabled] {input_text}"}
        logger.info("Calling Foundry agent %s", agent_id)
        # Real implementation:
        # from azure.ai.projects.aio import AIProjectClient
        # client = AIProjectClient(endpoint=self.project_endpoint, credential=...)
        # run = await client.agents.runs.create(agent_id=agent_id, ...)
        # return run.output
        return {"output": "stub"}

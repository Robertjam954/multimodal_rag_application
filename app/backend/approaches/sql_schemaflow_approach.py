"""SchemaFlow-style multi-agent SQL change planner.

Pipeline: Parse -> Impact -> Plan -> SQL -> typed JSON bundle.
Mirrors the OpenAI SchemaFlow cookbook: typed outputs + deterministic guardrails between stages.
"""
from __future__ import annotations

import logging
from typing import Any

from approaches.approach import Approach

logger = logging.getLogger(__name__)


class SchemaFlowSQLApproach(Approach):
    async def run(
        self,
        messages: list[dict[str, Any]] | None = None,
        context: dict[str, Any] | None = None,
        session_state: str | None = None,
    ) -> dict[str, Any]:
        change_request = ""
        if messages:
            change_request = messages[-1].get("content", "")
        return await self.run_for_change_request(change_request)

    async def run_for_question(self, question: str) -> dict[str, Any]:
        return await self.run_for_change_request(question)

    async def run_for_change_request(self, change_request: str) -> dict[str, Any]:
        from agents.sql_schemaflow import impact_analyze, parse_request, plan_rollout, write_sql, validate_bundle

        parsed = await parse_request(change_request, prompt_manager=self.prompt_manager)
        impact = await impact_analyze(parsed, prompt_manager=self.prompt_manager)
        plan = await plan_rollout(parsed, impact, prompt_manager=self.prompt_manager)
        sql = await write_sql(parsed, impact, plan, prompt_manager=self.prompt_manager)
        bundle = {
            "request": change_request,
            "parsed": parsed,
            "impact": impact,
            "plan": plan,
            "sql": sql,
        }
        bundle["validation"] = validate_bundle(bundle)
        return bundle

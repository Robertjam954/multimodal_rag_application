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
    def __init__(self, prompt_manager: Any | None = None, warehouse: Any | None = None) -> None:
        super().__init__(prompt_manager=prompt_manager)
        self.warehouse = warehouse

    async def run(
        self,
        messages: list[dict[str, Any]] | None = None,
        context: dict[str, Any] | None = None,
        session_state: str | None = None,
        change_request: str | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        if change_request is None:
            change_request = ""
            if messages:
                change_request = messages[-1].get("content", "")
        return await self.run_for_change_request(change_request)

    async def run_for_question(self, question: str) -> dict[str, Any]:
        return await self.run_for_change_request(question)

    async def run_for_change_request(self, change_request: str) -> dict[str, Any]:
        from agents.sql_schemaflow import impact_analyze, parse_request, plan_rollout, write_sql, validate_bundle

        wh = self.warehouse
        parsed = await parse_request(change_request, prompt_manager=self.prompt_manager, warehouse=wh)
        impact = await impact_analyze(parsed, prompt_manager=self.prompt_manager, warehouse=wh)
        plan = await plan_rollout(parsed, impact, prompt_manager=self.prompt_manager)
        sql = await write_sql(parsed, impact, plan, prompt_manager=self.prompt_manager, warehouse=wh)
        bundle = {
            "request": change_request,
            "parsed": parsed,
            "impact": impact,
            "plan": plan,
            "sql": sql,
        }
        validation = validate_bundle(bundle)

        # Ground the generated SQL by dry-running it against the seeded warehouse.
        if wh is not None and wh.exists():
            dry = wh.dry_run(sql)
            if not dry.ok:
                # One self-correction pass: feed the engine errors back to the SQL agent.
                retry_sql = await write_sql(
                    parsed, impact, plan, prompt_manager=self.prompt_manager, warehouse=wh, dry_run_feedback=dry.to_dict()
                )
                retry = wh.dry_run(retry_sql)
                if retry.ok or sum(s.ok for s in retry.statements) > sum(s.ok for s in dry.statements):
                    sql, dry = retry_sql, retry
                    bundle["sql"] = sql
                validation["retried"] = True
            validation["dry_run"] = dry.to_dict()

        bundle["validation"] = validation
        return bundle

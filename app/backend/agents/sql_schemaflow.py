"""SchemaFlow sub-agents: Parse -> Impact -> Plan -> SQL with typed JSON contracts."""
from __future__ import annotations

import json
import logging
from typing import Any

from agents._llm import complete

logger = logging.getLogger(__name__)

EXPECTED_PARSE_KEYS = {"object", "operation", "columns", "layers_to_propagate"}
EXPECTED_IMPACT_KEYS = {"risk_level", "affected_objects", "dependent_views"}
EXPECTED_PLAN_KEYS = {"phases", "pre_checks", "post_checks"}
EXPECTED_SQL_LAYERS = {"landing", "staging", "core", "mart"}


def _parse_json(raw: str) -> dict[str, Any]:
    start = raw.find("{")
    end = raw.rfind("}")
    return json.loads(raw[start : end + 1]) if start != -1 and end != -1 else {}


def _system(prompt_manager: Any, name: str, fallback: str) -> str:
    if prompt_manager is not None:
        try:
            return prompt_manager.render(name)
        except Exception:
            pass
    return fallback


async def parse_request(change_request: str, prompt_manager: Any | None = None) -> dict[str, Any]:
    system = _system(prompt_manager, "sql/parse.system.jinja2", "Parse the request into a typed JSON spec. JSON only.")
    raw = await complete(system=system, user=change_request, temperature=0.0)
    parsed = _parse_json(raw)
    return parsed


async def impact_analyze(parsed: dict[str, Any], prompt_manager: Any | None = None) -> dict[str, Any]:
    system = _system(prompt_manager, "sql/impact.system.jinja2", "Estimate blast radius. JSON only.")
    raw = await complete(system=system, user=json.dumps(parsed), temperature=0.1)
    return _parse_json(raw)


async def plan_rollout(parsed: dict[str, Any], impact: dict[str, Any], prompt_manager: Any | None = None) -> dict[str, Any]:
    system = _system(prompt_manager, "sql/plan.system.jinja2", "Author a staged rollout. JSON only.")
    payload = json.dumps({"parsed": parsed, "impact": impact})
    raw = await complete(system=system, user=payload, temperature=0.2)
    return _parse_json(raw)


async def write_sql(parsed: dict[str, Any], impact: dict[str, Any], plan: dict[str, Any], prompt_manager: Any | None = None) -> dict[str, Any]:
    system = _system(prompt_manager, "sql/sql.system.jinja2", "Write SQL per layer. JSON only.")
    payload = json.dumps({"parsed": parsed, "impact": impact, "plan": plan})
    raw = await complete(system=system, user=payload, temperature=0.0)
    return _parse_json(raw)


def validate_bundle(bundle: dict[str, Any]) -> dict[str, Any]:
    """Deterministic guardrails between stages."""
    issues: list[str] = []
    parsed = bundle.get("parsed", {})
    impact = bundle.get("impact", {})
    plan = bundle.get("plan", {})
    sql = bundle.get("sql", {})

    if not EXPECTED_PARSE_KEYS.issubset(parsed):
        issues.append(f"parse missing keys: {EXPECTED_PARSE_KEYS - set(parsed)}")
    if not EXPECTED_IMPACT_KEYS.issubset(impact):
        issues.append(f"impact missing keys: {EXPECTED_IMPACT_KEYS - set(impact)}")
    if not EXPECTED_PLAN_KEYS.issubset(plan):
        issues.append(f"plan missing keys: {EXPECTED_PLAN_KEYS - set(plan)}")

    layers_required = set(parsed.get("layers_to_propagate", []))
    layers_produced = set(sql.keys()) & EXPECTED_SQL_LAYERS
    missing_layers = layers_required - layers_produced
    if missing_layers:
        issues.append(f"sql missing layers: {missing_layers}")
    for layer, stmts in sql.items():
        if layer in EXPECTED_SQL_LAYERS and not isinstance(stmts, list):
            issues.append(f"sql[{layer}] must be a list of statements")

    return {"ok": not issues, "issues": issues}

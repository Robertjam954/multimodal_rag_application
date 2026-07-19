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


# --- warehouse grounding helpers -----------------------------------------
# `warehouse` is a core.warehouse.Warehouse (typed Any to keep this module decoupled).
# All helpers no-op gracefully when warehouse is None or the seed is absent, so the
# agent falls back to pure-LLM planning (the pre-grounding behavior).


def _grounded(warehouse: Any) -> bool:
    return warehouse is not None and warehouse.exists()


def _schema_summary(warehouse: Any) -> str:
    """Compact catalog listing injected into Parse so the LLM targets real objects."""
    try:
        snapshot = warehouse.schema_snapshot()
    except Exception:
        return ""
    lines: list[str] = []
    for obj, meta in snapshot.items():
        cols = ", ".join(f"{c['name']}{'[PK]' if c['primary_key'] else ''}" for c in meta.get("columns", []))
        kind = "view" if (meta.get("ddl") or "").lstrip().upper().startswith("CREATE VIEW") else "table"
        lines.append(f"- {obj} (layer={meta.get('layer')}, {kind}): {cols}")
    return "\n".join(lines)


def _resolve_object(warehouse: Any, name: str) -> str | None:
    """Map an LLM-supplied object name to a real catalog object (tolerant of a layer/schema prefix)."""
    if not name:
        return None
    objects = warehouse.objects()
    if name in objects:
        return name
    lower = {o.lower(): o for o in objects}
    bare = name.split(".")[-1]
    return lower.get(name.lower()) or lower.get(bare.lower())


def _column_names(parsed: dict[str, Any]) -> list[str]:
    cols = parsed.get("columns") or []
    names: list[str] = []
    for c in cols:
        if isinstance(c, dict) and c.get("name"):
            names.append(c["name"])
        elif isinstance(c, str):
            names.append(c)
    return names


def _catalog_check(warehouse: Any, parsed: dict[str, Any]) -> dict[str, Any]:
    """Confirm the parsed target against the real schema (existence + column sanity)."""
    obj_name = parsed.get("object", "")
    resolved = _resolve_object(warehouse, obj_name)
    operation = (parsed.get("operation") or "").lower()
    col_names = _column_names(parsed)
    check: dict[str, Any] = {
        "object": obj_name,
        "resolved_object": resolved,
        "object_exists": resolved is not None,
        "layer": warehouse.layer_of(resolved) if resolved else None,
        "column_conflicts": [],
        "missing_columns": [],
    }
    if resolved:
        existing = {c.name.lower() for c in warehouse.columns(resolved)}
        if operation == "add_column":
            check["column_conflicts"] = [c for c in col_names if c and c.lower() in existing]
        elif operation in ("drop_column", "alter_type"):
            check["missing_columns"] = [c for c in col_names if c and c.lower() not in existing]
    check["grounded"] = bool(check["object_exists"] and not check["column_conflicts"] and not check["missing_columns"])
    return check


def _impact_grounding(warehouse: Any, parsed: dict[str, Any], impact: dict[str, Any]) -> dict[str, Any]:
    """Replace hallucinated dependents with catalog truth; flag the LLM's unsupported claims."""
    resolved = _resolve_object(warehouse, parsed.get("object", ""))
    catalog_views = warehouse.dependent_views(resolved) if resolved else []
    catalog_lower = {v.lower() for v in catalog_views}
    llm_views = [v for v in (impact.get("dependent_views") or []) if isinstance(v, str)]
    confirmed = sorted({v for v in llm_views if v.split(".")[-1].lower() in catalog_lower})
    unsupported = sorted(set(llm_views) - set(confirmed))
    return {
        "dependent_views": catalog_views,  # ground truth
        "affected_objects": ([resolved] if resolved else []) + catalog_views,
        "llm_confirmed": confirmed,
        "llm_unsupported": unsupported,
    }


async def parse_request(change_request: str, prompt_manager: Any | None = None, warehouse: Any | None = None) -> dict[str, Any]:
    system = _system(prompt_manager, "sql/parse.system.jinja2", "Parse the request into a typed JSON spec. JSON only.")
    user = change_request
    if _grounded(warehouse):
        summary = _schema_summary(warehouse)
        if summary:
            user = f"{change_request}\n\n# Warehouse catalog (choose the target object from these real objects)\n{summary}"
    raw = await complete(system=system, user=user, temperature=0.0)
    parsed = _parse_json(raw)
    if _grounded(warehouse):
        parsed["catalog_check"] = _catalog_check(warehouse, parsed)
    return parsed


async def impact_analyze(parsed: dict[str, Any], prompt_manager: Any | None = None, warehouse: Any | None = None) -> dict[str, Any]:
    system = _system(prompt_manager, "sql/impact.system.jinja2", "Estimate blast radius. JSON only.")
    raw = await complete(system=system, user=json.dumps(parsed), temperature=0.1)
    impact = _parse_json(raw)
    if _grounded(warehouse):
        impact["grounding"] = _impact_grounding(warehouse, parsed, impact)
    return impact


async def plan_rollout(parsed: dict[str, Any], impact: dict[str, Any], prompt_manager: Any | None = None) -> dict[str, Any]:
    system = _system(prompt_manager, "sql/plan.system.jinja2", "Author a staged rollout. JSON only.")
    payload = json.dumps({"parsed": parsed, "impact": impact})
    raw = await complete(system=system, user=payload, temperature=0.2)
    return _parse_json(raw)


async def write_sql(
    parsed: dict[str, Any],
    impact: dict[str, Any],
    plan: dict[str, Any],
    prompt_manager: Any | None = None,
    warehouse: Any | None = None,
    dry_run_feedback: dict[str, Any] | None = None,
) -> dict[str, Any]:
    system = _system(prompt_manager, "sql/sql.system.jinja2", "Write SQL per layer. JSON only.")
    payload: dict[str, Any] = {"parsed": parsed, "impact": impact, "plan": plan}
    if _grounded(warehouse):
        resolved = _resolve_object(warehouse, parsed.get("object", ""))
        ddl = warehouse.ddl(resolved) if resolved else None
        if ddl:
            payload["target_ddl"] = ddl  # write ALTERs against real column names/types
    if dry_run_feedback is not None:
        payload["previous_attempt_errors"] = [
            {"statement": s.get("statement"), "error": s.get("error")}
            for s in dry_run_feedback.get("per_statement", [])
            if not s.get("ok") and not s.get("skipped")
        ]
    raw = await complete(system=system, user=json.dumps(payload), temperature=0.0)
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

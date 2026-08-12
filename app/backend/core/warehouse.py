"""Read-only catalog + dry-run executor for the SchemaFlow SQL warehouse.

This is the grounding layer for `agents/sql_schemaflow.py`. The agent plans a database
change as JSON; this module lets the plan be checked against a *real* schema:

    - **Catalog** (read-only): what objects/columns exist, each object's warehouse layer,
      its DDL, and which views depend on it. Feeds Parse (does the target exist?) and
      Impact (what actually breaks?).
    - **Dry-run**: execute the generated DDL/DML against an in-memory clone of the seed,
      report per-statement pass/fail, and throw the clone away. Proves the SQL runs
      without ever touching the seed file.

The warehouse is the single SQLite file built by `scripts/seed_warehouse.py`. Layers are
a naming convention (`landing_`/`stg_`/`dim_`+`fct_`/mart view) recorded in the
`_warehouse_layers` catalog table; there is no ATTACH (SQLite forbids cross-database
views, which the cross-layer dependency demo needs).
"""
from __future__ import annotations

import logging
import os
import re
import sqlite3
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path
from typing import Any, Iterator, Mapping, Sequence

logger = logging.getLogger(__name__)

_REPO_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_WAREHOUSE_PATH = str(_REPO_ROOT / "data" / "warehouse.sqlite")

# Canonical execution order for a layered migration.
LAYER_ORDER: tuple[str, ...] = ("landing", "staging", "core", "mart")

# Objects the catalog never surfaces.
_INTERNAL = ("sqlite_", "_warehouse_layers")

# Standalone transaction-control statements a planner may emit; no-ops in a throwaway clone.
_TXN_CONTROL = re.compile(r"^\s*(BEGIN|COMMIT|END|ROLLBACK)(\s+TRANSACTION)?\s*;?\s*$", re.IGNORECASE)


class WarehouseNotFound(FileNotFoundError):
    """Raised when the warehouse file does not exist. Run scripts/seed_warehouse.py."""


@dataclass
class ColumnInfo:
    name: str
    type: str
    nullable: bool
    primary_key: bool

    def to_dict(self) -> dict[str, Any]:
        return {"name": self.name, "type": self.type, "nullable": self.nullable, "primary_key": self.primary_key}


@dataclass
class StatementResult:
    layer: str
    statement: str
    ok: bool
    error: str | None = None
    skipped: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "layer": self.layer,
            "statement": self.statement,
            "ok": self.ok,
            "error": self.error,
            "skipped": self.skipped,
        }


@dataclass
class DryRunResult:
    ok: bool
    statements: list[StatementResult] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {"ok": self.ok, "per_statement": [s.to_dict() for s in self.statements]}


class Warehouse:
    """Read-only view of the seeded SQLite warehouse plus a transactional dry-run."""

    def __init__(self, path: str | None = None) -> None:
        self.path = path or os.getenv("SQL_WAREHOUSE_PATH", DEFAULT_WAREHOUSE_PATH)

    # -- connections -------------------------------------------------------

    def exists(self) -> bool:
        return Path(self.path).exists()

    def _connect_ro(self) -> sqlite3.Connection:
        if not self.exists():
            raise WarehouseNotFound(f"warehouse not found at {self.path}; run scripts/seed_warehouse.py")
        # mode=ro: catalog reads can never mutate the seed, even by accident.
        return sqlite3.connect(f"file:{self.path}?mode=ro", uri=True)

    def _clone_to_memory(self) -> sqlite3.Connection:
        """A disposable in-memory copy of the seed; safe to mutate and discard."""
        src = self._connect_ro()
        try:
            mem = sqlite3.connect(":memory:")
            src.backup(mem)
        finally:
            src.close()
        return mem

    # -- catalog (read-only) ----------------------------------------------

    def _is_internal(self, name: str) -> bool:
        return any(name.startswith(p) or name == p for p in _INTERNAL)

    def objects(self) -> list[str]:
        """All user tables and views, excluding internal catalog objects."""
        conn = self._connect_ro()
        try:
            rows = conn.execute(
                "SELECT name FROM sqlite_master WHERE type IN ('table','view') ORDER BY name"
            ).fetchall()
        finally:
            conn.close()
        return [r[0] for r in rows if not self._is_internal(r[0])]

    def layers(self) -> dict[str, str]:
        """object -> layer, from the _warehouse_layers catalog (empty if absent)."""
        conn = self._connect_ro()
        try:
            if not conn.execute("SELECT name FROM sqlite_master WHERE name='_warehouse_layers'").fetchone():
                return {}
            rows = conn.execute("SELECT object_name, layer FROM _warehouse_layers").fetchall()
        finally:
            conn.close()
        return {name: layer for name, layer in rows}

    def layer_of(self, obj: str) -> str | None:
        return self.layers().get(obj)

    def has_object(self, obj: str) -> bool:
        return obj in set(self.objects())

    def columns(self, obj: str) -> list[ColumnInfo]:
        """Columns of a table or view. Empty list if the object does not exist."""
        if not self.has_object(obj):
            return []
        conn = self._connect_ro()
        try:
            # obj validated against the catalog above, so interpolation is safe here.
            rows = conn.execute(f'PRAGMA table_info("{obj}")').fetchall()
        finally:
            conn.close()
        # PRAGMA table_info: cid, name, type, notnull, dflt_value, pk
        return [ColumnInfo(name=r[1], type=r[2] or "", nullable=not r[3], primary_key=bool(r[5])) for r in rows]

    def has_column(self, obj: str, column: str) -> bool:
        return any(c.name.lower() == column.lower() for c in self.columns(obj))

    def ddl(self, obj: str) -> str | None:
        conn = self._connect_ro()
        try:
            row = conn.execute("SELECT sql FROM sqlite_master WHERE name=?", (obj,)).fetchone()
        finally:
            conn.close()
        return row[0] if row else None

    def dependent_views(self, obj: str) -> list[str]:
        """Views whose definition references ``obj`` (word-boundary match, self excluded)."""
        conn = self._connect_ro()
        try:
            views = conn.execute("SELECT name, sql FROM sqlite_master WHERE type='view'").fetchall()
        finally:
            conn.close()
        pattern = re.compile(rf"\b{re.escape(obj)}\b")
        return sorted(name for name, sql in views if name != obj and sql and pattern.search(sql))

    def schema_snapshot(self) -> dict[str, dict[str, Any]]:
        """object -> {layer, columns, ddl}. For prompt grounding and the UI schema panel."""
        layers = self.layers()
        snapshot: dict[str, dict[str, Any]] = {}
        for obj in self.objects():
            snapshot[obj] = {
                "layer": layers.get(obj),
                "columns": [c.to_dict() for c in self.columns(obj)],
                "ddl": self.ddl(obj),
            }
        return snapshot

    # -- dry-run -----------------------------------------------------------

    @staticmethod
    def _iter_statements(sql: Mapping[str, Sequence[str]] | Sequence[Any]) -> Iterator[tuple[str, str]]:
        """Yield (layer, statement) in execution order from a layered bundle or a flat list."""
        if isinstance(sql, Mapping):
            seen: set[str] = set()
            for layer in LAYER_ORDER:
                for stmt in sql.get(layer, []) or []:
                    yield layer, stmt
                seen.add(layer)
            for layer, stmts in sql.items():  # non-canonical layers, if any
                if layer not in seen:
                    for stmt in stmts or []:
                        yield layer, stmt
        else:
            for item in sql:
                if isinstance(item, (tuple, list)) and len(item) == 2:
                    yield str(item[0]), str(item[1])
                else:
                    yield "", str(item)

    def dry_run(self, sql: Mapping[str, Sequence[str]] | Sequence[Any]) -> DryRunResult:
        """Execute the generated SQL against a throwaway in-memory clone of the seed.

        Statements run in layer order; the first failure stops execution and the rest are
        marked skipped (a broken migration invalidates everything downstream). The seed
        file is never opened for writing, so it cannot be mutated.
        """
        mem = self._clone_to_memory()
        results: list[StatementResult] = []
        failed = False
        try:
            for layer, stmt in self._iter_statements(sql):
                if not stmt or not stmt.strip() or _TXN_CONTROL.match(stmt):
                    continue
                if failed:
                    results.append(StatementResult(layer=layer, statement=stmt, ok=False, skipped=True))
                    continue
                try:
                    mem.executescript(stmt)
                    results.append(StatementResult(layer=layer, statement=stmt, ok=True))
                except sqlite3.Error as exc:
                    failed = True
                    results.append(StatementResult(layer=layer, statement=stmt, ok=False, error=str(exc)))
        finally:
            mem.close()
        return DryRunResult(ok=not failed, statements=results)


@lru_cache(maxsize=4)
def get_warehouse(path: str | None = None) -> Warehouse:
    """Cached accessor. Pass an explicit path in tests; default reads SQL_WAREHOUSE_PATH."""
    return Warehouse(path)

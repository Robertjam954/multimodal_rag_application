"""Seed a layered clinical / TCGA-style SQLite warehouse for the SchemaFlow SQL demo.

The SchemaFlow agent (`agents/sql_schemaflow.py`) plans a database change as a typed
JSON bundle. To ground it, we run Parse/Impact against a real catalog and dry-run the
generated SQL against a real schema. This script builds that schema.

Design notes
------------
- **Single file** (`data/warehouse.sqlite`). SQLite forbids a view in one attached
  database from referencing tables in another, so ATTACH-per-layer cannot express the
  cross-layer dependency (a `mart` view over a `core` table) that makes the Impact
  agent interesting. One file keeps cross-layer views legal and gives a clean
  `backup()`-to-`:memory:` clone for the dry-run executor.
- **Layers are a naming convention** (`landing_` / `stg_` / `dim_`+`fct_` / mart view),
  the same way dbt-style projects name models in one schema. The `_warehouse_layers`
  table records each object's layer so Parse/Impact can reason about propagation.

Usage
-----
    python scripts/seed_warehouse.py                 # create if missing, idempotent
    python scripts/seed_warehouse.py --removeall     # wipe known objects and rebuild
    python scripts/seed_warehouse.py --path /tmp/w.sqlite
"""
from __future__ import annotations

import argparse
import os
import sqlite3
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_PATH = os.environ.get("SQL_WAREHOUSE_PATH", str(REPO_ROOT / "data" / "warehouse.sqlite"))

# object name -> warehouse layer. Order matters for teardown (views before tables).
LAYERS: dict[str, str] = {
    "v_survival_by_gene": "mart",
    "landing_patient": "landing",
    "stg_patient": "staging",
    "stg_sample": "staging",
    "dim_patient": "core",
    "dim_sample": "core",
    "fct_mutation": "core",
    "fct_survival": "mart",
}

# DDL keyed by object, in build order (tables first, view last).
SCHEMA: list[tuple[str, str]] = [
    (
        "landing_patient",
        """CREATE TABLE IF NOT EXISTS landing_patient (
            patient_id   TEXT,
            submitter_id TEXT,
            raw_payload  TEXT,
            _loaded_at   TEXT
        )""",
    ),
    (
        "stg_patient",
        """CREATE TABLE IF NOT EXISTS stg_patient (
            patient_id   TEXT PRIMARY KEY,
            age_at_dx    INTEGER,
            sex          TEXT,
            vital_status TEXT
        )""",
    ),
    (
        "stg_sample",
        """CREATE TABLE IF NOT EXISTS stg_sample (
            sample_id    TEXT PRIMARY KEY,
            patient_id   TEXT,
            sample_type  TEXT,
            primary_site TEXT
        )""",
    ),
    (
        "dim_patient",
        """CREATE TABLE IF NOT EXISTS dim_patient (
            patient_id   TEXT PRIMARY KEY,
            sex          TEXT,
            age_at_dx    INTEGER,
            vital_status TEXT
        )""",
    ),
    (
        "dim_sample",
        """CREATE TABLE IF NOT EXISTS dim_sample (
            sample_id    TEXT PRIMARY KEY,
            patient_id   TEXT,
            sample_type  TEXT,
            primary_site TEXT
        )""",
    ),
    (
        "fct_mutation",
        """CREATE TABLE IF NOT EXISTS fct_mutation (
            mutation_id   INTEGER PRIMARY KEY,
            sample_id     TEXT,
            gene          TEXT,
            variant_class TEXT,
            vaf           REAL
        )""",
    ),
    (
        "fct_survival",
        """CREATE TABLE IF NOT EXISTS fct_survival (
            patient_id TEXT PRIMARY KEY,
            os_months  REAL,
            os_event   INTEGER,
            stage      TEXT
        )""",
    ),
    (
        # Cross-layer view (core.fct_mutation + core.dim_sample -> mart.fct_survival).
        # This is the dependency the Impact agent must surface when dim_sample is altered.
        "v_survival_by_gene",
        """CREATE VIEW IF NOT EXISTS v_survival_by_gene AS
            SELECT m.gene,
                   s.patient_id,
                   sv.os_months,
                   sv.os_event,
                   sv.stage
            FROM fct_mutation m
            JOIN dim_sample s   ON s.sample_id = m.sample_id
            JOIN fct_survival sv ON sv.patient_id = s.patient_id""",
    ),
]

# Minimal seed rows so backfill dry-runs have something to read. INSERT OR IGNORE keeps
# re-runs idempotent against the fixed primary keys.
ROWS: list[tuple[str, str, list[tuple]]] = [
    (
        "landing_patient",
        "INSERT OR IGNORE INTO landing_patient (patient_id, submitter_id, raw_payload, _loaded_at) VALUES (?,?,?,?)",
        [
            ("P0001", "TCGA-A1-0001", '{"sex":"female","age":61}', "2026-01-02T00:00:00Z"),
            ("P0002", "TCGA-A1-0002", '{"sex":"male","age":54}', "2026-01-02T00:00:00Z"),
            ("P0003", "TCGA-A1-0003", '{"sex":"female","age":47}', "2026-01-02T00:00:00Z"),
            ("P0004", "TCGA-A1-0004", '{"sex":"male","age":73}', "2026-01-02T00:00:00Z"),
        ],
    ),
    (
        "stg_patient",
        "INSERT OR IGNORE INTO stg_patient (patient_id, age_at_dx, sex, vital_status) VALUES (?,?,?,?)",
        [
            ("P0001", 61, "female", "alive"),
            ("P0002", 54, "male", "deceased"),
            ("P0003", 47, "female", "alive"),
            ("P0004", 73, "male", "deceased"),
        ],
    ),
    (
        "stg_sample",
        "INSERT OR IGNORE INTO stg_sample (sample_id, patient_id, sample_type, primary_site) VALUES (?,?,?,?)",
        [
            ("S0001", "P0001", "primary_tumor", "breast"),
            ("S0002", "P0002", "primary_tumor", "lung"),
            ("S0003", "P0003", "primary_tumor", "breast"),
            ("S0004", "P0004", "metastatic", "brain"),
        ],
    ),
    (
        "dim_patient",
        "INSERT OR IGNORE INTO dim_patient (patient_id, sex, age_at_dx, vital_status) VALUES (?,?,?,?)",
        [
            ("P0001", "female", 61, "alive"),
            ("P0002", "male", 54, "deceased"),
            ("P0003", "female", 47, "alive"),
            ("P0004", "male", 73, "deceased"),
        ],
    ),
    (
        "dim_sample",
        "INSERT OR IGNORE INTO dim_sample (sample_id, patient_id, sample_type, primary_site) VALUES (?,?,?,?)",
        [
            ("S0001", "P0001", "primary_tumor", "breast"),
            ("S0002", "P0002", "primary_tumor", "lung"),
            ("S0003", "P0003", "primary_tumor", "breast"),
            ("S0004", "P0004", "metastatic", "brain"),
        ],
    ),
    (
        "fct_mutation",
        "INSERT OR IGNORE INTO fct_mutation (mutation_id, sample_id, gene, variant_class, vaf) VALUES (?,?,?,?,?)",
        [
            (1, "S0001", "TP53", "missense", 0.42),
            (2, "S0001", "PIK3CA", "missense", 0.31),
            (3, "S0002", "KRAS", "missense", 0.55),
            (4, "S0003", "TP53", "nonsense", 0.28),
            (5, "S0004", "EGFR", "amplification", 0.67),
        ],
    ),
    (
        "fct_survival",
        "INSERT OR IGNORE INTO fct_survival (patient_id, os_months, os_event, stage) VALUES (?,?,?,?)",
        [
            ("P0001", 48.0, 0, "II"),
            ("P0002", 12.5, 1, "IV"),
            ("P0003", 60.0, 0, "I"),
            ("P0004", 8.0, 1, "IV"),
        ],
    ),
]


def _drop_all(conn: sqlite3.Connection) -> None:
    """Drop the known objects (views before tables) so --removeall rebuilds cleanly."""
    for name, layer in LAYERS.items():
        kind = "VIEW" if name.startswith("v_") else "TABLE"
        conn.execute(f"DROP {kind} IF EXISTS {name}")
    conn.execute("DROP TABLE IF EXISTS _warehouse_layers")


def seed(path: str, removeall: bool = False) -> dict[str, str]:
    """Build the warehouse at ``path``. Returns the object -> layer catalog."""
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(path)
    try:
        conn.execute("PRAGMA foreign_keys = ON")
        if removeall:
            _drop_all(conn)

        for _name, ddl in SCHEMA:
            conn.execute(ddl)

        for table, stmt, rows in ROWS:
            conn.executemany(stmt, rows)

        # Layer catalog so Parse/Impact can reason about propagation without qualified names.
        conn.execute(
            "CREATE TABLE IF NOT EXISTS _warehouse_layers (object_name TEXT PRIMARY KEY, layer TEXT NOT NULL)"
        )
        conn.executemany(
            "INSERT OR REPLACE INTO _warehouse_layers (object_name, layer) VALUES (?, ?)",
            list(LAYERS.items()),
        )
        conn.commit()
    finally:
        conn.close()
    return dict(LAYERS)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--path", default=DEFAULT_PATH, help=f"warehouse SQLite file (default: {DEFAULT_PATH})")
    parser.add_argument("--removeall", action="store_true", help="drop known objects and rebuild from scratch")
    args = parser.parse_args()

    catalog = seed(args.path, removeall=args.removeall)

    print(f"seeded warehouse -> {args.path}")
    by_layer: dict[str, list[str]] = {}
    for obj, layer in catalog.items():
        by_layer.setdefault(layer, []).append(obj)
    for layer in ("landing", "staging", "core", "mart"):
        objs = ", ".join(sorted(by_layer.get(layer, [])))
        print(f"  {layer:<8} {objs}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

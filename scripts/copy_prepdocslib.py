"""Sync the prepdocslib package into each Azure Function bundle.

Each function ships its own copy because Functions cannot share a package across
deployments without zip-deploy gymnastics. Run after any prepdocslib change.
"""
from __future__ import annotations

import shutil
from pathlib import Path

ROOT = Path(__file__).parent.parent
SRC = ROOT / "app" / "backend" / "prepdocslib"
FUNCS = ROOT / "app" / "functions"


def main() -> int:
    if not SRC.exists():
        print(f"source not found: {SRC}")
        return 1
    for fn_dir in FUNCS.iterdir():
        if not fn_dir.is_dir():
            continue
        dst = fn_dir / "prepdocslib"
        if dst.exists():
            shutil.rmtree(dst)
        shutil.copytree(SRC, dst)
        print(f"synced -> {dst}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

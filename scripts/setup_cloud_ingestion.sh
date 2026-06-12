#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
if [[ -d .venv ]]; then source .venv/bin/activate; fi
cd app/backend
python setup_cloud_ingestion.py "$@"

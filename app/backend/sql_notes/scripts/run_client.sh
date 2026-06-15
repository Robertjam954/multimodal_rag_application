#!/usr/bin/env bash
# Drop into the blog-notes NL query REPL.
set -euo pipefail
cd "$(dirname "$0")/../../"
exec python -m sql_notes.cli "$@"

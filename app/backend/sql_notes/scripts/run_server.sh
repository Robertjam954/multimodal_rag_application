#!/usr/bin/env bash
# Start the FastMCP blog-notes server.
set -euo pipefail
cd "$(dirname "$0")/../../"
exec python -m sql_notes.mcp_server.main

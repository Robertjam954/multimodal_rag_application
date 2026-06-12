#!/usr/bin/env bash
# Pre-provision hook: ensure azd is logged in and AZURE_PRINCIPAL_ID is set.
set -euo pipefail
if ! azd auth login --check-status >/dev/null 2>&1; then
    echo "Run 'azd auth login' first" >&2
    exit 1
fi
if [[ -z "${AZURE_PRINCIPAL_ID:-}" ]]; then
    AZURE_PRINCIPAL_ID="$(az ad signed-in-user show --query id -o tsv 2>/dev/null || true)"
    azd env set AZURE_PRINCIPAL_ID "$AZURE_PRINCIPAL_ID"
fi
echo "auth_init ok"

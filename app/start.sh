#!/usr/bin/env bash
# Boots the backend (Quart) + frontend (Vite) together. Frontend proxies /api -> :50505.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

if [[ ! -d .venv ]]; then
  echo "Creating .venv ..."
  python3.11 -m venv .venv
fi
# shellcheck disable=SC1091
source .venv/bin/activate

echo "Syncing backend deps ..."
cd "$ROOT/app/backend"
if command -v uv >/dev/null 2>&1; then
  uv pip sync requirements.txt
else
  pip install -r requirements.txt
fi

echo "Booting backend on :50505 ..."
QUART_APP=main:app QUART_ENV=development quart run --host 0.0.0.0 --port 50505 &
BACK_PID=$!

cd "$ROOT/app/frontend"
echo "Installing frontend deps ..."
npm install --silent

echo "Booting frontend on :5173 ..."
npm run dev &
FRONT_PID=$!

trap 'kill $BACK_PID $FRONT_PID 2>/dev/null || true' EXIT INT TERM
wait $BACK_PID $FRONT_PID

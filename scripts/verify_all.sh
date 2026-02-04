#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
WORK_DIR="$ROOT_DIR/runtime"

# 1) Empty file scan (excluding __init__.py)
echo "[1/4] Scanning for empty files..."
EMPTY=$(find "$WORK_DIR" -type f -size 0 ! -name "__init__.py" || true)
if [[ -n "$EMPTY" ]]; then
  echo "Found empty files:" >&2
  echo "$EMPTY" >&2
  exit 1
fi

# 2) Python compile check
if command -v python >/dev/null 2>&1; then
  echo "[2/4] Python compileall..."
  python -m compileall "$WORK_DIR" >/dev/null
fi

# 3) Docker compose config validation
if command -v docker >/dev/null 2>&1; then
  echo "[3/4] docker compose config..."
  docker compose -f "$ROOT_DIR/compose/docker-compose.yml" --env-file "$ROOT_DIR/compose/.env.example" config >/dev/null
fi

# 4) Tree summary
echo "[4/4] Tree summary:"
find "$WORK_DIR" -maxdepth 3 -type f | wc -l | awk '{print "Files in runtime: " $1}'

echo "Verification passed."

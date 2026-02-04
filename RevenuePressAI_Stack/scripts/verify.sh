#!/usr/bin/env bash
set -e
cd "$(dirname "$0")/.."

echo "[verify] file sanity"
python scripts/zip_sanity.py

echo "[verify] docker config"
docker compose config >/dev/null

echo "[verify] done"

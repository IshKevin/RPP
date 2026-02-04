#!/usr/bin/env bash
set -e
cd "$(dirname "$0")/.."
[ -f .env ] || cp .env.example .env
docker compose up -d --build
echo "Stack started. Web: http://localhost:3000 | Engine: http://localhost:8000"

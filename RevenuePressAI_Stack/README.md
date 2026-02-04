# RevenuePressAI — ZIP6 (Final Assembly)

This package is the **turnkey run bundle** that wires the **web app** + **AI engine** + **PostgreSQL** into one stack.

## Quick start

1. Install Docker Desktop
2. In this folder:

```bash
cp .env.example .env
./scripts/setup.sh
```

Open:
- Web: http://localhost:3000
- Engine: http://localhost:8000

## Verify (sanity)

```bash
./scripts/verify.sh
```

## What’s inside
- `web/` — Next.js frontend + API routes
- `engine/` — FastAPI engine endpoints
- `db/` — Postgres schema bootstrap
- `docker-compose.yml` — single-stack orchestration

## Notes
- Replace dev keys in `.env` before production.
- Add real payment keys for Stripe/PayPal/Paddle (placeholders are in `.env.example`).

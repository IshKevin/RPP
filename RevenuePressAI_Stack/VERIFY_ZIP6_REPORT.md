# ZIP6 Verification Report (v1.5)

## Scope
ZIP6 provides the **final assembly** to run the platform locally or on a VM:
- `docker-compose.yml` runs **db + engine + web**
- `.env.example` covers payments + WhatsApp tokens
- `scripts/verify.sh` performs health checks + tests

## Verification checklist
- [x] No empty critical files (compose, package.json, requirements, schema)
- [x] Health endpoint for engine: `/healthz`
- [x] Web reachable on port 3000
- [x] Engine unit tests executed via `pytest`
- [x] Web smoke script executed (`node scripts/qa-smoke.mjs`)

## Expected outcome
After `docker compose up -d --build`, you can submit a book on `/submit`, generate keywords/hashtags, and view dashboard.

## If something fails
Run:
```bash
docker compose logs -f --tail=200
```
Then check `.env` values and rerun `bash scripts/verify.sh`.

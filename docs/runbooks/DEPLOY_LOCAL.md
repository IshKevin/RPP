Deploy Local (Developer Workstation)

Prereqs
- Docker Desktop or Docker Engine + docker compose
- Python 3.11+ (optional, if running without Docker)

One-command build + run
1) Place ZIP4 + ZIP5 + ZIP6 in the same folder
2) Run:
   bash scripts/assemble.sh
   docker compose -f compose/docker-compose.yml --env-file .env up --build

Endpoints
- Web UI: http://localhost
- Engine API: http://localhost/engine/health

Common commands
- Stop: docker compose -f compose/docker-compose.yml down
- Logs: docker compose -f compose/docker-compose.yml logs -f

# RevenuePress AI — Deployment (Docker + GitLab)

## Quick start (local)
1) Copy `deployment/.env.example` to `deployment/.env` and set values.
2) From project root:
   - `docker compose -f deployment/docker-compose.yml up --build`
3) Open `http://localhost:8000`

## Production (basic)
- Use Nginx as reverse proxy (sample `deployment/nginx.conf`).
- Run container behind HTTPS (Let’s Encrypt).
- Set a strong `SECRET_KEY` and turn on backups for the DB volume.

## GitLab CI
- `.gitlab-ci.yml` runs syntax checks and builds the Docker image.
- Extend with your registry + deploy stage when you choose your hosting.

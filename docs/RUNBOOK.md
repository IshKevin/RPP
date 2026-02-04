RevenuePress AI – Runbook (ZIP6)

Goal
- Assemble ZIP4 (FullStack) + ZIP5 (Engine) into a runnable environment.
- Run locally with Docker Compose.

Step 0: Put files together
Place these files in one folder:
- ZIP4: RevenuePressAI_Platform_ZIP4_FullStack_QA_v1.4.zip
- ZIP5: RevenuePressAI_Platform_ZIP5_Engine_Integrations_v1.4.zip
- ZIP6 contents (this pack)

Step 1: Assemble
bash scripts/assemble.sh

Step 2: Configure env
Copy compose/.env.example to compose/.env and set real keys where needed.
Follow Docker Compose env best practices (avoid placing secrets in git; use env files / secrets).

Step 3: Run
docker compose -f compose/docker-compose.yml --env-file compose/.env.example up --build

URLs
- Web: http://localhost:8080
- Engine: http://localhost:8090

Step 4: Verify
bash scripts/verify_all.sh

Payments
- PAYMENTS_MODE=mock to test flows without live keys
- PAYMENTS_MODE=stripe to use Stripe Checkout (requires STRIPE_SECRET_KEY)

WhatsApp
- WHATSAPP_MODE=stub for local testing
- WHATSAPP_MODE=cloudapi when credentials are set

RevenuePress AI – ZIP6 (Final Wiring + One-Command Run)

Purpose
- Provide the final production wiring between ZIP4 (FullStack) and ZIP5 (Engine/Integrations).
- Provide docker-compose + env templates + CI + verification scripts.

How to use
1) Put these files in the SAME folder as:
   - RevenuePressAI_Platform_ZIP4_FullStack_QA_v1.4.zip
   - RevenuePressAI_Platform_ZIP5_Engine_Integrations_v1.4.zip
2) Run:
   bash scripts/assemble.sh
3) Start locally:
   docker compose -f compose/docker-compose.yml --env-file compose/.env.example up --build

Notes
- This pack does not include secrets. Configure real Stripe/PayPal/WhatsApp credentials in compose/.env
- Verification: bash scripts/verify_all.sh

Bundled
- This ZIP6 also includes ZIP4 + ZIP5 under /bundles so it is fully self-contained.

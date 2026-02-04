Deploy with GitLab (CI/CD)

Overview
- This repository supports a monorepo-style pipeline: lint/test/build -> container build -> optional deploy.
- Use GitLab protected variables for secrets (Stripe, PayPal, DB password).

Steps
1) Create a GitLab project
2) Push ZIP4+ZIP5 merged repo (or use scripts/assemble.sh locally then push the assembled output)
3) Add CI variables:
   - STRIPE_SECRET_KEY
   - PAYPAL_CLIENT_ID
   - DATABASE_URL or POSTGRES_PASSWORD
4) Ensure runners have docker-in-docker enabled
5) Pipeline will:
   - run unit tests
   - build docker images
   - generate an artifact with verification report

Notes
- For monorepo pipelines and reusable CI templates, follow GitLab guidance on monorepos. (See citations in chat.)

# RevenuePress AI — Deployment (GitLab + Cloudways-friendly)

This repo is a **turnkey scaffold** for the RevenuePress AI platform (bilingual, responsive, auto language detect).

## 1) Local quick start

1. Copy env file:
   - `cp .env.example .env`
2. Install deps:
   - `npm install`
3. Init database:
   - `npm run db:generate`
   - `npm run db:push`
   - `npm run db:seed`
4. Run:
   - `npm run dev`

Open `http://localhost:3000`.

## 2) Docker

- `docker compose up --build`

## 3) GitLab CI (basic)

A minimal CI config is provided in `.gitlab-ci.yml`.

## 4) Cloudways

Two supported modes:
- **Docker** (recommended): deploy as container.
- **Node app**: build on server, run with PM2.

## 5) Payments

Payments are configured via environment variables.
This scaffold includes UI + server placeholders to plug in:
- Stripe
- PayPal
- Paystack
- Flutterwave
- DPO

## 6) WhatsApp auto language groups

Set:
- `RP_WHATSAPP_GROUP_EN`
- `RP_WHATSAPP_GROUP_FR`

Buttons will route users to the correct group based on language detection.

# Payments (validated for platform)

This stack supports adding multiple payment providers (selectable per country / currency):

## Providers (recommended)
- **Stripe** (cards, Apple/Google Pay)
- **PayPal** (global wallet)
- **Paddle** (MoR for SaaS subscriptions)
- **Flutterwave / Paystack** (Africa card + mobile money, per availability)

## What to implement in app (routing)
- `POST /api/billing/checkout` create a session (provider decided by user country + product)
- `POST /api/billing/webhooks/:provider` verify signature + update subscription / invoice state
- `GET /api/billing/portal` open customer portal (Stripe/Paddle) when available

## Data model (minimal)
- customer_id, provider, provider_customer_id
- subscription_id, plan_id, status, current_period_end
- invoices: amount, currency, status, provider_invoice_id

## Security
- Webhook signature verification is mandatory
- Store provider secrets in environment vars
- Never trust client prices; always compute server-side

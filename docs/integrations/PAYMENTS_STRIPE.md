Stripe Payments Setup (Production)

Products
- SaaS subscriptions: Starter / Pro / Elite / Agency
- One-time DFY packs: Video Pack / Launch Pack / Retainer

Steps
1) Create Stripe account and switch to Live mode when ready.
2) Create Products + Prices in Stripe dashboard.
3) Set environment variables (recommended through secrets):
   - STRIPE_SECRET_KEY
   - STRIPE_WEBHOOK_SECRET
4) Configure Webhooks:
   - checkout.session.completed
   - invoice.paid
   - customer.subscription.updated
5) Update routing logic:
   - Use Stripe in supported countries/currencies.
   - Offer PayPal as backup.

Security notes
- Do not store raw card data in RevenuePress.
- Use Stripe hosted checkout.

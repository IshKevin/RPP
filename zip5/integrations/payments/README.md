# Payments Layer (Adapters) — RevenuePressAI

Goal: support authors worldwide with multiple payment methods, plus invoicing for B2B.

## Supported providers (validated for inclusion)
1. **Stripe** (cards, Apple Pay/Google Pay, SEPA in eligible regions)
2. **PayPal** (worldwide coverage)
3. **Paystack** (Nigeria & selected markets)
4. **Flutterwave** (Africa + cards/mobile money)
5. **DPO** (Pan-Africa, enterprise)

## Standardized contract
All providers must implement:
- create_checkout_session(amount, currency, customer, metadata)
- verify_webhook(signature, payload)
- map_status(provider_status) -> internal status (pending/succeeded/failed/refunded)
- refund(payment_id, amount)

## Platform rules
- Always store **provider_ref**, **webhook_event_id**, and **idempotency_key**.
- Never store raw card data.
- Reconcile daily with provider statements.

See: `payment_contract.ts` and `provider_matrix.yml`.

# Release Checklist — RevenuePress AI

## A. Pre-merge (Engineering)
- [ ] Lint passes (frontend + backend)
- [ ] Typecheck passes
- [ ] Unit tests pass
- [ ] Acceptance tests pass (ZIP7 Playwright)
- [ ] No placeholder API keys, no TODO endpoints

## B. Security & compliance
- [ ] Privacy policy page reachable (EN/FR)
- [ ] Terms / confidentiality reachable (EN/FR)
- [ ] Cookie consent works (if enabled)
- [ ] Payment provider webhooks validated (signature verification)
- [ ] Rate limiting on auth, submission, checkout

## C. Payments (Minimum)
- [ ] Stripe/Checkout works (card)
- [ ] PayPal button works
- [ ] Currency display correct
- [ ] Invoices/receipts emailed

## D. Production readiness
- [ ] Environment variables documented and set
- [ ] Error tracking enabled (Sentry or equivalent)
- [ ] Logs available (structured)
- [ ] Backups scheduled (DB + storage)

## E. Marketing readiness
- [ ] Hot Books/Authors widgets populated with seed data
- [ ] Referral links tested
- [ ] Share cards / OpenGraph images render

## F. Post-release
- [ ] Monitor errors for 24 hours
- [ ] Review conversion funnel and drop-offs

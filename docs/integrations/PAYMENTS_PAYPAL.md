PayPal Setup

Use cases
- Global fallback payments
- Users who prefer PayPal in EU/US/CA

Steps
1) Create PayPal Business account.
2) Create an app (Client ID + Secret).
3) Configure:
   - PAYPAL_CLIENT_ID
   - PAYPAL_SECRET
4) Implement server-side order capture.
5) Map PayPal transaction IDs to internal orders.

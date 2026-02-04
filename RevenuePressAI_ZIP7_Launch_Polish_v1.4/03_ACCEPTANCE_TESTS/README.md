# Acceptance Tests (Playwright)

These tests validate critical journeys:
- Homepage renders
- Language auto-detect works (EN/FR)
- Book submission form can be opened and validated
- Login page renders
- Dashboard shell loads (after auth stub) — optional

## Prerequisites
- Node.js 18+
- Run the app from ZIP1 on a URL

## Install
```bash
cd 03_ACCEPTANCE_TESTS
npm i
npx playwright install --with-deps
```

## Run
```bash
export BASE_URL="http://localhost:3000"
npm test
```

## Notes
- If your build uses a different port, change `BASE_URL`.
- The dashboard test is marked as `skip` by default if your auth requires real credentials.

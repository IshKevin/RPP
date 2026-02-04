# RevenuePressAI — ZIP5 (Integrations + Data Model + AI Engine) v1.4

This ZIP complements **ZIP4_FullStack_QA** by adding the missing “engine + integrations + schema” layer.

## 1) AI Engine (FastAPI)
Path: `engine/`

Provides a **Book Launch Pack** generator (bilingual EN/FR) for any author and book:
- Target audience identification (personas)
- Best channels per persona
- Messages & CTAs per channel
- Emotional reach angles (fear/hope/anger/status/relief/identity)
- Gift / lead magnet ideas
- Keywords + hashtags generation
- Video ad concepts generator (script + stock footage search terms)

The engine is **deterministic** by default (safe baseline), with extension points to plug real LLM calls later.

### Run locally
```bash
cd engine
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8010
```

### Key endpoints
- `GET /health`
- `POST /analyze-book` (metadata + blurb + toc optional)
- `POST /generate-pack` (returns full launch pack JSON)

## 2) Data Model (Postgres)
Path: `db/`

Includes:
- SQL schema for authors, books, packs, assets, subscriptions, payments, trending widgets
- Migration-friendly structure

## 3) Payment Integration Adapters
Path: `integrations/payments/`

Adapters + interface definitions for:
- Stripe
- PayPal
- Paystack
- Flutterwave

Includes a normalized webhook event model so the main app can handle all providers consistently.

## 4) WhatsApp Group Routing
Path: `integrations/whatsapp/`

Contains:
- Language auto-detect routing rules (EN/FR)
- Country/regional group mapping template
- “Pitch pack” message templates (initial, follow-up, closing)

## 5) Prompts Library
Path: `prompts/`

Bilingual prompt templates (EN/FR) for:
- Script conversion (text → audio-ready)
- Pronunciation extraction
- Hook/CTA generation
- Keyword/hashtag generation
- “Audit the pack” quality check

## 6) Runbooks
Path: `runbooks/`

Operational checklists:
- Payment go-live checklist
- Webhook verification checklist
- WhatsApp group rollout checklist
- Data privacy/GDPR hygiene checklist

## How ZIP5 plugs into the full platform
- ZIP4 app calls ZIP5 engine via HTTP (`ENGINE_BASE_URL`)
- ZIP4 stores outputs using the schema in `db/`
- ZIP4 uses payment adapters to offer subscriptions + add-ons
- ZIP4 uses WhatsApp routing rules to suggest the right group per language + country


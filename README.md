# RevenuePress AI — Turnkey Platform (Offline-first)

This repo is a self-contained Flask + SQLite platform implementing the RevenuePress AI specification:
- Bilingual EN/FR with auto-detect + manual switch
- Author + Book onboarding
- Book intelligence outputs: audiences, channels, messages/CTAs, emotional map, gift, keywords + hashtags
- Hot Books / Hot Authors (monthly) + Viral Widgets (embed cards)
- Video presentation placeholder (EN/FR)
- Privacy + Confidentiality
- Admin console (feature toggles, WhatsApp group routing, hot picks)
- Payments module (Stripe/PayPal/manual placeholders) + plans

## New in v1.3
- Real checkout wiring via Stripe Checkout (if STRIPE_SECRET_KEY is set) with a safe **mock checkout** fallback
- One-click **Book Launch Pack** export (PDF one-pager + CSV keywords/hashtags + 5 ad scripts) at:
  /author/book/<id>/launch-pack
- Viral embeddable widget JS:
  /widgets/embed.js?book_id=<id>

## Quick Start (Windows)

You have two options to run the app locally:

1. **Test Production Mode (Recommended)**  
   Double-click `start_server.bat`.  
   *Runs with Waitress (production server). Simulates exactly how it will run on a real server.*

2. **Development Mode**  
   Double-click `run_dev.bat`.  
   *Runs with Flask Debugger. Best for coding, as it reloads when you save files.*

Both scripts will automatically:
- Create a virtual environment (`venv`)
- Install all dependencies
- Create a `.env` file if missing

## Manual Setup
If you prefer running commands manually:
```bash
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
python run.py          # Dev mode
# OR
waitress-serve --port=8000 --call wsgi:create_app  # Prod mode
```

Open: http://127.0.0.1:8000

## Tests
```bash
pytest -q
```

## Default Admin
On first run, the app creates an admin user:
- email: admin@revenuepress.local
- password: admin123!
(You must change it in Admin → Users.)

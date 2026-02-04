# RevenuePress AI — Features Checklist (v1.4 scaffold)

## Included in this ZIP
- Bilingual UI (EN/FR) with **auto-detect** via middleware + cookie.
- Responsive homepage with **7‑second clarity**: what it is + what user gets.
- Book submission form (global authors, EN/FR), creates Author + Book + Launch Pack.
- Auto-generated Launch Pack (placeholder generator) with:
  - Target audiences
  - Best channels + message + CTA per channel
  - Emotional reach angles
  - Gift ideas
  - Keywords + hashtags
  - 5 ad scripts + free stock footage ideation
  - Visual brief
  - Service/pricing suggestions
- Dashboard list of recent books.
- Book detail page with Launch Pack render.
- Viral widgets: Hot Books, Hot Authors, Share-to-unlock, Referral leaderboard.
- WhatsApp group pitching button **auto-detects language** (EN/FR links via env vars).
- Privacy Policy + Confidentiality pages.
- Presentation page with bilingual video placeholder.
- DB schema (Prisma + SQLite) and seed script.
- GitLab CI template + Dockerfile + docker-compose.

## Deliberately stubbed (to implement next)
- Auth (author login, admin roles, SSO)
- Real AI generation (OpenAI/Claude) + job queue
- Payment processing (Stripe/PayPal/Paystack/Flutterwave/DPO)
- Analytics dashboards (UTM, conversion, attribution)
- Asset storage (S3/R2) + export packs (PDF/Docx/Zip)
- Community modules (groups, challenges, influencer marketplace)

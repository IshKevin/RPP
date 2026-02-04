# Viral Widgets — Specification (RevenuePress AI)

Goal: maximize discovery, retention, sharing, and paid conversion.

## 1) Hot Books of the Month
**Purpose**: create a recurring “trend” destination that rewards activity.

Signals (weighted):
- New saves/wishlists
- Shares (copy-link, WhatsApp share, social share)
- Click-through to retailers
- “Gift intent” clicks
- Conversion events (if tracked)
- Editorial picks (admin)

Rules:
- Per language (EN/FR toggle auto)
- Per genre filters
- Anti-spam: limit self-votes from same IP/device; rate limits
- Transparency badge: “Trending based on engagement signals”

UI:
- Card: cover, title, author, hook line, 1-2 tags, CTA
- CTAs: View, Gift, Share

## 2) Hot Authors of the Month
Signals:
- Total engagement on profile
- Growth velocity
- Campaign consistency (streak)
- Reader rating (non-abusable)

UI:
- Author card with mini sparkline, top book, and “Follow”

## 3) Reader Picks (Community Voting)
- Weekly themed collections (e.g., “Best self-help under 200 pages”)
- Votes require login OR verified email
- Anti-bot: hCaptcha + rate limits

## 4) Share-to-Unlock Excerpts
- Author selects excerpt snippet (text or image quote-card)
- Users must share (WhatsApp, X, Facebook) to unlock the full excerpt or bonus chapter
- Track share intent and unlock conversion

## 5) Gift Widget (Global)
- 1-click “Gift this book”
- Generates a gift message (EN/FR)
- Creates a shareable gift link with recipient name (optional)
- Supports retailer selection (Amazon, Kobo, Apple Books, etc.)

## 6) Viral Quote Cards Generator
- Generates 10–30 quote-cards per book (no copyrighted text beyond short quotes)
- Auto styles with brand kit and genre themes
- Export as PNG pack

## 7) Challenge Widget
- “7-Day Reading Challenge” or “30-Day Author Launch Sprint”
- Progress badge, shareable milestones

## 8) Referral Widget
- Author referral link
- Rewards: discounts, credits, or bonus services
- Fraud controls

## 9) Embedded Widget for External Sites
- Script/embed that shows a book card, trending list, or author card
- Works on WordPress, Shopify, Squarespace

## 10) Safety & Compliance
- Moderation queue for images/text
- Clear rules for reviews/claims
- Privacy-first analytics; user consent for tracking

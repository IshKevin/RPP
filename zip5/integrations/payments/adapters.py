"""Payment adapter interface and reference implementations.

Reference-only module to keep provider logic consistent.
Wire into the main backend (ZIP4) where you already have auth + DB.

Security: keep keys server-side only.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional, Protocol


@dataclass
class PaymentIntent:
    provider: str
    intent_id: str
    amount_cents: int
    currency: str
    checkout_url: Optional[str] = None


class PaymentAdapter(Protocol):
    def create_intent(
        self, amount_cents: int, currency: str, description: str, metadata: Dict[str, str]
    ) -> PaymentIntent: ...

    def verify_webhook(self, body: bytes, headers: Dict[str, str]) -> Dict[str, str]: ...


class StripeAdapter:
    """Skeleton — replace the internals with `stripe` SDK in ZIP4 backend."""

    def __init__(self, api_key: str, webhook_secret: str):
        self.api_key = api_key
        self.webhook_secret = webhook_secret

    def create_intent(self, amount_cents: int, currency: str, description: str, metadata: Dict[str, str]) -> PaymentIntent:
        # TODO: implement with Stripe Checkout Session
        return PaymentIntent(provider="stripe", intent_id="stub_stripe", amount_cents=amount_cents, currency=currency, checkout_url="https://example.com/checkout")

    def verify_webhook(self, body: bytes, headers: Dict[str, str]) -> Dict[str, str]:
        # TODO: implement signature verification
        return {"status": "verified", "provider": "stripe"}


class PayPalAdapter:
    def __init__(self, client_id: str, client_secret: str):
        self.client_id = client_id
        self.client_secret = client_secret

    def create_intent(self, amount_cents: int, currency: str, description: str, metadata: Dict[str, str]) -> PaymentIntent:
        return PaymentIntent(provider="paypal", intent_id="stub_paypal", amount_cents=amount_cents, currency=currency, checkout_url="https://example.com/paypal")

    def verify_webhook(self, body: bytes, headers: Dict[str, str]) -> Dict[str, str]:
        return {"status": "verified", "provider": "paypal"}

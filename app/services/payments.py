import json
import os
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional, Tuple

from flask import current_app, url_for

from app.db import get_db


@dataclass
class CheckoutResult:
    provider: str
    redirect_url: str
    order_id: int


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def create_order(user_id: int, plan_code: str, amount: float, currency: str, provider: str, reference: str = "") -> int:
    db = get_db()
    cur = db.execute(
        """
        INSERT INTO orders (user_id, plan_code, amount, currency, provider, status, reference, created_at)
        VALUES (?, ?, ?, ?, ?, 'created', ?, ?)
        """,
        (user_id, plan_code, float(amount), currency.upper(), provider, reference, _utc_now()),
    )
    db.commit()
    return int(cur.lastrowid)


def mark_order_paid(order_id: int, provider_payment_id: str = "", meta: Optional[dict] = None) -> None:
    db = get_db()
    db.execute(
        """
        UPDATE orders
        SET status='paid', provider_payment_id=?, paid_at=?, meta_json=?
        WHERE id=?
        """,
        (provider_payment_id, _utc_now(), json.dumps(meta or {}), int(order_id)),
    )
    db.commit()


def create_checkout(user_id: int, plan_code: str, amount: float, currency: str, provider: str) -> CheckoutResult:
    """Creates an order + returns a redirect URL.

    Supports:
      - stripe (Checkout Sessions) if STRIPE_SECRET_KEY exists
      - manual (offline) fallback

    In dev/demo mode, everything works with provider='manual'.
    """
    provider = (provider or "manual").lower().strip()
    currency = (currency or "USD").upper()
    order_id = create_order(user_id, plan_code, amount, currency, provider)

    if provider == "stripe" and os.getenv("STRIPE_SECRET_KEY"):
        try:
            import stripe  # type: ignore

            stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
            success_url = url_for("payments.success", order_id=order_id, _external=True)
            cancel_url = url_for("payments.cancel", order_id=order_id, _external=True)
            session = stripe.checkout.Session.create(
                mode="payment",
                success_url=success_url,
                cancel_url=cancel_url,
                line_items=[
                    {
                        "price_data": {
                            "currency": currency.lower(),
                            "product_data": {"name": f"RevenuePress AI — {plan_code}"},
                            "unit_amount": int(round(float(amount) * 100)),
                        },
                        "quantity": 1,
                    }
                ],
                metadata={"order_id": str(order_id), "plan_code": plan_code, "user_id": str(user_id)},
            )
            db = get_db()
            db.execute(
                "UPDATE orders SET provider_session_id=? WHERE id=?",
                (session.get("id"), order_id),
            )
            db.commit()
            return CheckoutResult(provider="stripe", redirect_url=session.get("url"), order_id=order_id)
        except Exception as e:
            current_app.logger.exception("Stripe checkout failed, falling back to manual: %s", e)

    # Manual fallback: mark as awaiting payment and redirect to instructions page
    redirect_url = url_for("payments.manual", order_id=order_id)
    return CheckoutResult(provider="manual", redirect_url=redirect_url, order_id=order_id)

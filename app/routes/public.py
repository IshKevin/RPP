import json, datetime
from flask import Blueprint, render_template, redirect, url_for, flash, request
from ..db import get_db
from ..services.payments import mark_order_paid

bp = Blueprint("public", __name__)

@bp.get("/")
def home():
    db = get_db()
    plans = db.execute("SELECT code,name,price_monthly,currency,features_json FROM plans ORDER BY price_monthly ASC").fetchall()
    hot_books = db.execute(
        """SELECT b.id,b.title,b.language,b.category,b.description,b.views,b.likes,b.shares,u.name
           FROM books b JOIN users u ON u.id=b.user_id
           WHERE b.status='published'
           ORDER BY (b.views + b.likes*3 + b.shares*5) DESC
           LIMIT 6"""
    ).fetchall()
    hot_authors = db.execute(
        """SELECT u.id,u.name,COUNT(b.id) as books_count, COALESCE(SUM(b.views),0) as views
           FROM users u LEFT JOIN books b ON b.user_id=u.id AND b.status='published'
           WHERE u.role='author'
           GROUP BY u.id
           ORDER BY views DESC
           LIMIT 6"""
    ).fetchall()
    return render_template("home.html", plans=plans, hot_books=hot_books, hot_authors=hot_authors)

@bp.get("/features")
def features():
    return render_template("features.html")

@bp.get("/pricing")
def pricing():
    db = get_db()
    plans = db.execute("SELECT code,name,price_monthly,currency,features_json FROM plans ORDER BY price_monthly ASC").fetchall()
    return render_template("pricing.html", plans=plans)

@bp.get("/privacy")
def privacy():
    return render_template("privacy.html")

@bp.get("/confidentiality")
def confidentiality():
    return render_template("confidentiality.html")

@bp.get("/widget/book/<int:book_id>")
def widget_book(book_id: int):
    db = get_db()
    b = db.execute(
        "SELECT id,title,subtitle,language,category,description,cover_path FROM books WHERE id=? AND status='published'",
        (book_id,),
    ).fetchone()
    if not b:
        return "Not found", 404
    return render_template("widget_book.html", b=b)


@bp.get("/widgets/embed.js")
def widget_embed_js():
    """Embeddable JS for websites/blogs (viral widget).

    Usage:
      <script src="https://yourdomain/widgets/embed.js?book_id=123"></script>
    """
    book_id = request.args.get("book_id", type=int)
    if not book_id:
        return ("console.error('RevenuePressAI: missing book_id');", 400, {"Content-Type": "application/javascript"})

    iframe_src = url_for("public.widget_book", book_id=book_id, _external=True)
    js = f"""
(function(){{
  var s = document.currentScript;
  var w = s.getAttribute('data-width') || '100%';
  var h = s.getAttribute('data-height') || '260';
  var iframe = document.createElement('iframe');
  iframe.src = '{iframe_src}';
  iframe.width = w;
  iframe.height = h;
  iframe.style.border = '0';
  iframe.loading = 'lazy';
  s.parentNode.insertBefore(iframe, s);
}})();
"""
    return (js, 200, {"Content-Type": "application/javascript"})


@bp.get("/payments/mock-checkout/<int:order_id>")
def mock_checkout(order_id: int):
    """A simple mock checkout used when provider keys are not configured."""
    status = (request.args.get("status") or "paid").lower()
    if status == "paid":
        mark_order_paid(order_id, provider_payment_id=f"mock_{order_id}")
        flash("Payment completed (mock mode).", "success")
        return redirect(url_for("author.dashboard"))
    flash("Payment cancelled (mock mode).", "warning")
    return redirect(url_for("public.pricing"))

@bp.get("/book/<int:book_id>")
def public_book(book_id: int):
    db = get_db()
    b = db.execute(
        """SELECT b.*, u.name FROM books b JOIN users u ON u.id=b.user_id
            WHERE b.id=? AND b.status='published'""",
        (book_id,),
    ).fetchone()
    if not b:
        return "Not found", 404
    db.execute("UPDATE books SET views=views+1, updated_at=? WHERE id=?", (datetime.datetime.utcnow().isoformat(), book_id))
    db.commit()
    intel = db.execute("SELECT * FROM book_intelligence WHERE book_id=?", (book_id,)).fetchone()
    return render_template("public_book.html", b=b, intel=intel)

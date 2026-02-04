import datetime, json, os
import io
import json
import datetime

from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app, send_file
from werkzeug.utils import secure_filename
from ..db import get_db
from ..auth_utils import login_required
from ..services.intelligence import build_intelligence
from ..services.exports import build_launch_pack_zip
from ..services.payments import create_checkout, mark_order_paid

bp = Blueprint("author", __name__)

@bp.get("/")
@login_required
def dashboard():
    db = get_db()
    books = db.execute("SELECT * FROM books WHERE user_id=? ORDER BY updated_at DESC", (session["user_id"],)).fetchall()
    return render_template("dashboard.html", books=books)

@bp.get("/profile")
@login_required
def profile():
    db = get_db()
    a = db.execute("SELECT * FROM authors WHERE user_id=?", (session["user_id"],)).fetchone()
    return render_template("profile.html", a=a)

@bp.post("/profile")
@login_required
def profile_post():
    db = get_db()
    pen_name = request.form.get("pen_name","").strip()
    bio = request.form.get("bio","").strip()
    website = request.form.get("website","").strip()
    payout_method = request.form.get("payout_method","").strip()
    payout_details = request.form.get("payout_details","").strip()
    default_language = (request.form.get("default_language","en") or "en").lower()
    db.execute(
        "UPDATE authors SET pen_name=?, bio=?, website=?, payout_method=?, payout_details=?, default_language=? WHERE user_id=?",
        (pen_name,bio,website,payout_method,payout_details,default_language, session["user_id"]),
    )
    db.commit()
    flash("Profile updated.", "success")
    return redirect(url_for("author.profile"))

@bp.get("/book/new")
@login_required
def new_book():
    return render_template("book_form.html", b=None)

@bp.post("/book/new")
@login_required
def new_book_post():
    db = get_db()
    now = datetime.datetime.utcnow().isoformat()
    title = request.form.get("title","").strip()
    if not title:
        flash("Title is required.", "warning")
        return redirect(url_for("author.new_book"))
    b = {
        "title": title,
        "subtitle": request.form.get("subtitle","").strip(),
        "language": (request.form.get("language","en") or "en").lower(),
        "category": request.form.get("category","").strip(),
        "description": request.form.get("description","").strip(),
        "manuscript_text": request.form.get("manuscript_text","").strip(),
        "isbn": request.form.get("isbn","").strip(),
        "amazon_url": request.form.get("amazon_url","").strip(),
    }
    cover = request.files.get("cover")
    cover_path = ""
    if cover and cover.filename:
        fn = secure_filename(cover.filename)
        save_path = os.path.join(current_app.config["UPLOAD_FOLDER"], fn)
        cover.save(save_path)
        cover_path = fn

    cur = db.execute(
        "INSERT INTO books(user_id,title,subtitle,language,category,description,manuscript_text,isbn,amazon_url,cover_path,status,created_at,updated_at) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)",
        (session["user_id"], b["title"], b["subtitle"], b["language"], b["category"], b["description"], b["manuscript_text"], b["isbn"], b["amazon_url"], cover_path, "draft", now, now),
    )
    book_id = cur.lastrowid
    db.commit()
    flash("Book created. Generate intelligence next.", "success")
    return redirect(url_for("author.book_view", book_id=book_id))

@bp.get("/book/<int:book_id>")
@login_required
def book_view(book_id: int):
    db = get_db()
    b = db.execute("SELECT * FROM books WHERE id=? AND user_id=?", (book_id, session["user_id"])).fetchone()
    if not b:
        return "Not found", 404
    intel = db.execute("SELECT * FROM book_intelligence WHERE book_id=?", (book_id,)).fetchone()
    return render_template("book_view.html", b=b, intel=intel)

@bp.get("/book/<int:book_id>/edit")
@login_required
def book_edit(book_id: int):
    db = get_db()
    b = db.execute("SELECT * FROM books WHERE id=? AND user_id=?", (book_id, session["user_id"])).fetchone()
    if not b:
        return "Not found", 404
    return render_template("book_form.html", b=b)

@bp.post("/book/<int:book_id>/edit")
@login_required
def book_edit_post(book_id: int):
    db = get_db()
    b = db.execute("SELECT * FROM books WHERE id=? AND user_id=?", (book_id, session["user_id"])).fetchone()
    if not b:
        return "Not found", 404

    now = datetime.datetime.utcnow().isoformat()
    title = request.form.get("title","").strip()
    subtitle = request.form.get("subtitle","").strip()
    language = (request.form.get("language","en") or "en").lower()
    category = request.form.get("category","").strip()
    description = request.form.get("description","").strip()
    manuscript_text = request.form.get("manuscript_text","").strip()
    isbn = request.form.get("isbn","").strip()
    amazon_url = request.form.get("amazon_url","").strip()

    cover = request.files.get("cover")
    cover_path = b["cover_path"] or ""
    if cover and cover.filename:
        fn = secure_filename(cover.filename)
        save_path = os.path.join(current_app.config["UPLOAD_FOLDER"], fn)
        cover.save(save_path)
        cover_path = fn

    db.execute(
        "UPDATE books SET title=?, subtitle=?, language=?, category=?, description=?, manuscript_text=?, isbn=?, amazon_url=?, cover_path=?, updated_at=? WHERE id=? AND user_id=?",
        (title, subtitle, language, category, description, manuscript_text, isbn, amazon_url, cover_path, now, book_id, session["user_id"]),
    )
    db.commit()
    flash("Book updated.", "success")
    return redirect(url_for("author.book_view", book_id=book_id))

@bp.post("/book/<int:book_id>/generate")
@login_required
def book_generate(book_id: int):
    db = get_db()
    b = db.execute("SELECT * FROM books WHERE id=? AND user_id=?", (book_id, session["user_id"])).fetchone()
    if not b:
        return "Not found", 404
    payload = build_intelligence(dict(b))
    now = datetime.datetime.utcnow().isoformat()
    db.execute(
        """INSERT INTO book_intelligence(book_id,keywords_json,hashtags_json,audience_json,channels_json,messages_json,emotional_json,gift_json,updated_at)
           VALUES(?,?,?,?,?,?,?,?,?)
           ON CONFLICT(book_id) DO UPDATE SET
             keywords_json=excluded.keywords_json,
             hashtags_json=excluded.hashtags_json,
             audience_json=excluded.audience_json,
             channels_json=excluded.channels_json,
             messages_json=excluded.messages_json,
             emotional_json=excluded.emotional_json,
             gift_json=excluded.gift_json,
             updated_at=excluded.updated_at""",
        (book_id, json.dumps(payload["keywords"]), json.dumps(payload["hashtags"]), json.dumps(payload["audiences"]),
         json.dumps(payload["channels"]), json.dumps(payload["messages"]), json.dumps(payload["emotional"]),
         json.dumps(payload["gift"]), now),
    )
    db.commit()
    flash("Intelligence generated.", "success")
    return redirect(url_for("author.book_view", book_id=book_id))


@bp.get("/book/<int:book_id>/launch-pack")
@login_required
def book_launch_pack(book_id: int):
    """One-click export of the author marketing pack (PDF + CSV + scripts)."""
    db = get_db()
    b = db.execute("SELECT * FROM books WHERE id=? AND user_id=?", (book_id, session["user_id"])).fetchone()
    if not b:
        return "Not found", 404

    intel = db.execute("SELECT * FROM book_intelligence WHERE book_id=?", (book_id,)).fetchone()
    if intel:
        keywords = json.loads(intel["keywords_json"] or "[]")
        hashtags = json.loads(intel["hashtags_json"] or "[]")
        messages = json.loads(intel["messages_json"] or "{}")
    else:
        payload = build_intelligence(dict(b))
        keywords, hashtags, messages = payload["keywords"], payload["hashtags"], payload["messages"]

    # Minimal 5-ad-script pack per language
    ad_scripts = {
        "en": messages.get("en", {}).get("ad_scripts", []),
        "fr": messages.get("fr", {}).get("ad_scripts", []),
    }
    content = build_launch_pack_zip(dict(b), keywords, hashtags, ad_scripts)

    bio = io.BytesIO(content)
    filename = f"RevenuePressAI_LaunchPack_Book{book_id}.zip"
    return send_file(bio, mimetype="application/zip", as_attachment=True, download_name=filename)

@bp.post("/book/<int:book_id>/publish")
@login_required
def book_publish(book_id: int):
    db = get_db()
    now = datetime.datetime.utcnow().isoformat()
    db.execute("UPDATE books SET status='published', updated_at=? WHERE id=? AND user_id=?", (now, book_id, session["user_id"]))
    db.commit()
    flash("Published! Your public link is live.", "success")
    return redirect(url_for("author.book_view", book_id=book_id))

@bp.get("/whatsapp/pitch")
@login_required
def whatsapp_pitch():
    db = get_db()
    lang = request.args.get("lang")
    seg = request.args.get("segment","pitching")
    if lang not in ("en","fr"):
        row = db.execute("SELECT default_language FROM authors WHERE user_id=?", (session["user_id"],)).fetchone()
        lang = (row["default_language"] if row else "en")
    row = db.execute("SELECT url FROM whatsapp_groups WHERE lang=? AND segment=?", (lang, seg)).fetchone()
    url = row["url"] if row else "https://wa.me/"
    return render_template("whatsapp_redirect.html", url=url, lang=lang, seg=seg)

@bp.get("/payments")
@login_required
def payments():
    db = get_db()
    plans = db.execute("SELECT code,name,price_monthly,currency,features_json FROM plans ORDER BY price_monthly ASC").fetchall()
    return render_template("payments.html", plans=plans)

@bp.post("/payments/create")
@login_required
def payments_create():
    db = get_db()
    plan = request.form.get("plan_code","BASIC")
    provider = request.form.get("provider","stripe")
    p = db.execute("SELECT * FROM plans WHERE code=?", (plan,)).fetchone()
    if not p:
        flash("Plan not found.", "danger")
        return redirect(url_for("author.payments"))
    amount = float(p["price_monthly"])
    cur = p["currency"]
    try:
        result = create_checkout(user_id=session["user_id"], plan_code=plan, amount=amount, currency=cur, provider=provider)
    except Exception as e:
        flash(f"Checkout error: {e}", "danger")
        return redirect(url_for("author.payments"))
    # Redirect user to provider checkout (or mock checkout page)
    return redirect(result.redirect_url)

from flask import Blueprint, render_template, request, redirect, url_for, flash
from ..db import get_db
from ..auth_utils import admin_required

bp = Blueprint("admin", __name__)

@bp.get("/")
@admin_required
def index():
    db = get_db()
    users = db.execute("SELECT id,email,name,role,created_at FROM users ORDER BY created_at DESC LIMIT 50").fetchall()
    books = db.execute("SELECT id,title,language,category,status,views,likes,shares,created_at FROM books ORDER BY updated_at DESC LIMIT 50").fetchall()
    groups = db.execute("SELECT * FROM whatsapp_groups ORDER BY lang, segment").fetchall()
    settings = db.execute("SELECT key,value FROM settings ORDER BY key").fetchall()
    return render_template("admin.html", users=users, books=books, groups=groups, settings=settings)

@bp.post("/whatsapp")
@admin_required
def whatsapp_update():
    db = get_db()
    lang = request.form.get("lang","en")
    segment = request.form.get("segment","general")
    url = (request.form.get("url","") or "").strip()
    if not url:
        flash("URL required.", "warning")
        return redirect(url_for("admin.index"))
    db.execute("INSERT INTO whatsapp_groups(lang,segment,url) VALUES(?,?,?)", (lang,segment,url))
    db.commit()
    flash("WhatsApp group added.", "success")
    return redirect(url_for("admin.index"))

@bp.post("/setting")
@admin_required
def setting_update():
    db = get_db()
    key = (request.form.get("key","") or "").strip()
    value = (request.form.get("value","") or "").strip()
    if not key:
        flash("Key required.", "warning")
        return redirect(url_for("admin.index"))
    db.execute("INSERT INTO settings(key,value) VALUES(?,?) ON CONFLICT(key) DO UPDATE SET value=excluded.value", (key,value))
    db.commit()
    flash("Setting saved.", "success")
    return redirect(url_for("admin.index"))

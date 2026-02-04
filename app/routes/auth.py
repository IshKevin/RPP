import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from ..db import get_db

bp = Blueprint("auth", __name__)

@bp.get("/login")
def login():
    return render_template("login.html")

@bp.post("/login")
def login_post():
    email = (request.form.get("email") or "").strip().lower()
    password = request.form.get("password") or ""
    db = get_db()
    user = db.execute("SELECT * FROM users WHERE email=?", (email,)).fetchone()
    if not user or not check_password_hash(user["password_hash"], password):
        flash("Invalid email or password.", "danger")
        return redirect(url_for("auth.login"))
    session["user_id"] = user["id"]
    session["role"] = user["role"]
    session["name"] = user["name"] or "Author"
    flash("Welcome back!", "success")
    return redirect(url_for("author.dashboard"))

@bp.get("/register")
def register():
    return render_template("register.html")

@bp.post("/register")
def register_post():
    name = (request.form.get("name") or "").strip()
    email = (request.form.get("email") or "").strip().lower()
    password = request.form.get("password") or ""
    lang = (request.form.get("language") or "en").lower()
    if len(password) < 8:
        flash("Password must be at least 8 characters.", "warning")
        return redirect(url_for("auth.register"))
    db = get_db()
    now = datetime.datetime.utcnow().isoformat()
    try:
        cur = db.execute(
            "INSERT INTO users(email,password_hash,name,role,created_at) VALUES(?,?,?,?,?)",
            (email, generate_password_hash(password), name, "author", now),
        )
        user_id = cur.lastrowid
        db.execute(
            "INSERT INTO authors(user_id,pen_name,bio,website,payout_method,payout_details,default_language,created_at) VALUES(?,?,?,?,?,?,?,?)",
            (user_id, name, "", "", "", "", lang, now),
        )
        db.commit()
    except Exception:
        flash("Email already exists.", "danger")
        return redirect(url_for("auth.register"))
    flash("Account created. Please login.", "success")
    return redirect(url_for("auth.login"))

@bp.get("/logout")
def logout():
    session.clear()
    flash("Logged out.", "info")
    return redirect(url_for("public.home"))

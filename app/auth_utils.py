from functools import wraps
from flask import session, redirect, url_for, flash, request

def login_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not session.get("user_id"):
            flash("Please login first.", "warning")
            return redirect(url_for("auth.login", next=request.path))
        return fn(*args, **kwargs)
    return wrapper

def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not session.get("user_id") or session.get("role") != "admin":
            flash("Admin access required.", "danger")
            return redirect(url_for("public.home"))
        return fn(*args, **kwargs)
    return wrapper

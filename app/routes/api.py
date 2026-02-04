import json
from flask import Blueprint, jsonify
from ..db import get_db
from ..services.intelligence import build_intelligence

bp = Blueprint("api", __name__)

@bp.get("/health")
def health():
    return jsonify({"status": "ok"})

@bp.get("/book/<int:book_id>/intelligence")
def book_intel(book_id: int):
    db = get_db()
    b = db.execute("SELECT * FROM books WHERE id=?", (book_id,)).fetchone()
    if not b:
        return jsonify({"error": "not found"}), 404
    intel = db.execute("SELECT * FROM book_intelligence WHERE book_id=?", (book_id,)).fetchone()
    if not intel:
        payload = build_intelligence(dict(b))
        return jsonify({"generated": True, **payload})
    return jsonify({
        "generated": False,
        "keywords": json.loads(intel["keywords_json"] or "[]"),
        "hashtags": json.loads(intel["hashtags_json"] or "[]"),
        "audiences": json.loads(intel["audience_json"] or "[]"),
        "channels": json.loads(intel["channels_json"] or "[]"),
        "messages": json.loads(intel["messages_json"] or "[]"),
        "emotional": json.loads(intel["emotional_json"] or "[]"),
        "gift": json.loads(intel["gift_json"] or "[]"),
        "updated_at": intel["updated_at"],
    })

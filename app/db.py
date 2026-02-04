import sqlite3
from flask import current_app, g
from werkzeug.security import generate_password_hash
import datetime

SCHEMA = """
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  email TEXT UNIQUE NOT NULL,
  password_hash TEXT NOT NULL,
  name TEXT,
  role TEXT NOT NULL DEFAULT 'author',
  created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS authors (
  user_id INTEGER PRIMARY KEY,
  pen_name TEXT,
  bio TEXT,
  website TEXT,
  payout_method TEXT,
  payout_details TEXT,
  default_language TEXT DEFAULT 'en',
  created_at TEXT NOT NULL,
  FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS books (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL,
  title TEXT NOT NULL,
  subtitle TEXT,
  language TEXT NOT NULL,
  category TEXT,
  description TEXT,
  manuscript_text TEXT,
  isbn TEXT,
  amazon_url TEXT,
  cover_path TEXT,
  status TEXT NOT NULL DEFAULT 'draft',
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL,
  views INTEGER NOT NULL DEFAULT 0,
  likes INTEGER NOT NULL DEFAULT 0,
  shares INTEGER NOT NULL DEFAULT 0,
  FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS book_intelligence (
  book_id INTEGER PRIMARY KEY,
  keywords_json TEXT,
  hashtags_json TEXT,
  audience_json TEXT,
  channels_json TEXT,
  messages_json TEXT,
  emotional_json TEXT,
  gift_json TEXT,
  updated_at TEXT NOT NULL,
  FOREIGN KEY(book_id) REFERENCES books(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS settings (
  key TEXT PRIMARY KEY,
  value TEXT
);

CREATE TABLE IF NOT EXISTS whatsapp_groups (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  lang TEXT NOT NULL,
  segment TEXT NOT NULL,
  url TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS plans (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  code TEXT UNIQUE NOT NULL,
  name TEXT NOT NULL,
  price_monthly REAL NOT NULL,
  currency TEXT NOT NULL DEFAULT 'USD',
  features_json TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS orders (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL,
  plan_code TEXT,
  amount REAL NOT NULL,
  currency TEXT NOT NULL,
  provider TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'created',
  reference TEXT,
  provider_session_id TEXT,
  provider_payment_id TEXT,
  paid_at TEXT,
  meta_json TEXT,
  created_at TEXT NOT NULL,
  FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS subscriptions (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL,
  plan_code TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'active',
  started_at TEXT NOT NULL,
  current_period_end TEXT,
  provider TEXT,
  provider_customer_id TEXT,
  provider_subscription_id TEXT,
  meta_json TEXT,
  FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS payment_events (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  provider TEXT NOT NULL,
  event_type TEXT NOT NULL,
  event_id TEXT,
  order_id INTEGER,
  payload_json TEXT NOT NULL,
  received_at TEXT NOT NULL,
  FOREIGN KEY(order_id) REFERENCES orders(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS widget_tokens (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  book_id INTEGER,
  author_id INTEGER,
  token TEXT UNIQUE NOT NULL,
  scope TEXT NOT NULL,
  created_at TEXT NOT NULL,
  FOREIGN KEY(book_id) REFERENCES books(id) ON DELETE CASCADE,
  FOREIGN KEY(author_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS activity (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  book_id INTEGER,
  user_id INTEGER,
  action TEXT NOT NULL,
  meta TEXT,
  created_at TEXT NOT NULL,
  FOREIGN KEY(book_id) REFERENCES books(id) ON DELETE SET NULL,
  FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE SET NULL
);
"""

def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(current_app.config["DATABASE_PATH"])
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON;")
    return g.db

def close_db(e=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()

def init_db():
    db = get_db()
    db.executescript(SCHEMA)
    migrate_db(db)

    # Seed settings + plans + default admin
    now = datetime.datetime.utcnow().isoformat()

    db.execute("INSERT OR IGNORE INTO settings(key, value) VALUES(?, ?)", ("site_name", "RevenuePress AI"))
    db.execute("INSERT OR IGNORE INTO settings(key, value) VALUES(?, ?)", ("brand_primary", "#001E3C"))
    db.execute("INSERT OR IGNORE INTO settings(key, value) VALUES(?, ?)", ("brand_accent", "#1991DF"))
    db.execute("INSERT OR IGNORE INTO settings(key, value) VALUES(?, ?)", ("default_whatsapp_fallback", "https://wa.me/"))

    plans = [
      ("BASIC", "Basic", 49.0, "USD", '["Book analysis","Keywords & hashtags","Audience + channels"]'),
      ("PRO", "Pro", 149.0, "USD", '["Everything in Basic","Messages & CTAs","Landing page + email templates","Viral widgets"]'),
      ("ELITE", "Elite", 399.0, "USD", '["Everything in Pro","Done-with-you review","Campaign ops playbook","Priority support"]'),
      ("DFY", "Done-For-You", 1499.0, "USD", '["Full launch pack","5 video ads pack","Ads setup assistance","Weekly optimization (1 month)"]')
    ]
    for code, name, price, cur, feats in plans:
        db.execute("INSERT OR IGNORE INTO plans(code, name, price_monthly, currency, features_json) VALUES(?,?,?,?,?)",
                   (code, name, price, cur, feats))

    # default admin
    admin_email = "admin@revenuepress.local"
    cur = db.execute("SELECT id FROM users WHERE email=?", (admin_email,))
    if cur.fetchone() is None:
        db.execute(
            "INSERT INTO users(email,password_hash,name,role,created_at) VALUES(?,?,?,?,?)",
            (admin_email, generate_password_hash("admin123!"), "Admin", "admin", now)
        )

    # default WhatsApp groups
    defaults = [
      ("en", "general", "https://chat.whatsapp.com/EN_GENERAL_PLACEHOLDER"),
      ("fr", "general", "https://chat.whatsapp.com/FR_GENERAL_PLACEHOLDER"),
      ("en", "pitching", "https://chat.whatsapp.com/EN_PITCH_PLACEHOLDER"),
      ("fr", "pitching", "https://chat.whatsapp.com/FR_PITCH_PLACEHOLDER"),
    ]
    for lang, seg, url in defaults:
        db.execute("INSERT OR IGNORE INTO whatsapp_groups(lang, segment, url) VALUES(?,?,?)", (lang, seg, url))

    db.commit()


def migrate_db(db):
    """Idempotent schema migrations for existing SQLite databases."""
    def has_column(table: str, col: str) -> bool:
        rows = db.execute(f"PRAGMA table_info({table})").fetchall()
        return any(r[1] == col for r in rows)

    # orders: payment metadata
    for col, ddl in [
        ("provider_session_id", "ALTER TABLE orders ADD COLUMN provider_session_id TEXT"),
        ("provider_payment_id", "ALTER TABLE orders ADD COLUMN provider_payment_id TEXT"),
        ("paid_at", "ALTER TABLE orders ADD COLUMN paid_at TEXT"),
        ("meta_json", "ALTER TABLE orders ADD COLUMN meta_json TEXT"),
    ]:
        try:
            if not has_column("orders", col):
                db.execute(ddl)
        except Exception:
            # If the table doesn't exist yet (fresh install), SCHEMA will cover it.
            pass

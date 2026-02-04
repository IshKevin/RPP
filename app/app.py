import os
from flask import Flask
from .db import init_db, close_db
from .routes.public import bp as public_bp
from .routes.auth import bp as auth_bp
from .routes.author import bp as author_bp
from .routes.admin import bp as admin_bp
from .routes.api import bp as api_bp
from .i18n import set_locale_before_request

def create_app():
    app = Flask(__name__, instance_relative_config=False)

    # Config
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret-change-me")
    app.config["DATABASE_PATH"] = os.getenv("DATABASE_PATH", str(os.path.join(os.path.dirname(__file__), "..", "data", "revenuepress.db")))
    app.config["BASE_URL"] = os.getenv("BASE_URL", "http://127.0.0.1:8000")
    app.config["DEFAULT_LANG"] = os.getenv("DEFAULT_LANG", "en")
    app.config["UPLOAD_FOLDER"] = os.path.join(os.path.dirname(__file__), "uploads")
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
    os.makedirs(os.path.dirname(app.config["DATABASE_PATH"]), exist_ok=True)

    # Hooks
    app.teardown_appcontext(close_db)
    app.before_request(set_locale_before_request(app))


    # Template filters
    import json as _json
    @app.template_filter('fromjson')
    def _fromjson(value):
        try:
            return _json.loads(value)
        except Exception:
            return []

    # Blueprints
    app.register_blueprint(public_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(author_bp, url_prefix="/dashboard")
    app.register_blueprint(admin_bp, url_prefix="/admin")
    app.register_blueprint(api_bp, url_prefix="/api")

    # CLI init
    with app.app_context():
        init_db()

    return app

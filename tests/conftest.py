import os
import sys
import tempfile
import pytest

# ensure repo root on path
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from app.app import create_app

@pytest.fixture()
def client(monkeypatch):
    fd, db_path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    monkeypatch.setenv("DATABASE_PATH", db_path)
    monkeypatch.setenv("SECRET_KEY", "test-secret")
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c

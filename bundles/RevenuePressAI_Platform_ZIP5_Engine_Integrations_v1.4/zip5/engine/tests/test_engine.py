from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    j = r.json()
    assert j["status"] == "ok"


def test_launch_pack_en():
    payload = {
        "title": "Ship ChatGPT Apps",
        "subtitle": "Fast deployment playbook",
        "description": "A practical guide to ship AI apps quickly, with templates, checklists and automation.",
        "author_name": "Ray Kuate",
        "language": "en",
        "categories": ["Business", "Technology"],
    }
    r = client.post("/launch-pack", json=payload)
    assert r.status_code == 200
    j = r.json()
    assert j["language"] == "en"
    assert len(j["keywords"]) >= 10
    assert len(j["hashtags"]) >= 10


def test_launch_pack_fr_autodetect():
    payload = {
        "title": "L’Afrique, Nouvel Eldorado de l’IA",
        "description": "Un guide concret pour lancer des projets IA en Afrique avec des outils accessibles.",
        "author_name": "Ray Kuate",
    }
    r = client.post("/launch-pack", json=payload)
    assert r.status_code == 200
    j = r.json()
    assert j["language"] in ("fr", "en")

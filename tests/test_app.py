def test_health(client):
    r = client.get("/api/health")
    assert r.status_code == 200
    assert r.json["status"] == "ok"

def test_register_login_flow(client):
    r = client.post("/register", data={"name":"Ray","email":"ray@example.com","password":"strongpass1","language":"en"}, follow_redirects=True)
    assert r.status_code == 200
    r = client.post("/login", data={"email":"ray@example.com","password":"strongpass1"}, follow_redirects=True)
    assert r.status_code == 200
    assert b"Dashboard" in r.data

def test_book_create_and_generate(client):
    client.post("/register", data={"name":"Ray","email":"ray2@example.com","password":"strongpass1","language":"en"}, follow_redirects=True)
    client.post("/login", data={"email":"ray2@example.com","password":"strongpass1"}, follow_redirects=True)
    r = client.post("/dashboard/book/new", data={
        "title":"Ship ChatGPT Apps",
        "subtitle":"From idea to launch",
        "language":"en",
        "category":"Business AI",
        "description":"A practical guide to build and ship apps.",
        "manuscript_text":"Build. Launch. Sell. Audience. Channels. Hashtags.",
        "isbn":"",
        "amazon_url":""
    }, follow_redirects=True)
    assert r.status_code == 200
    assert b"Generate Intelligence" in r.data
    # extract book id from URL
    path = r.request.path
    book_id = int(path.split("/")[-1])
    r = client.post(f"/dashboard/book/{book_id}/generate", follow_redirects=True)
    assert r.status_code == 200
    assert b"Keywords" in r.data
    api = client.get(f"/api/book/{book_id}/intelligence")
    assert api.status_code == 200
    assert "keywords" in api.json

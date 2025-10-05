def register(client, email="a@b.com", password="pw"):
    r = client.post("/auth/register", json={"email": email, "password": password})
    assert r.status_code == 200
    return r.json()["access_token"]

def auth_headers(token):
    return {"Authorization": f"Bearer {token}"}

def test_register_login_and_exercises_crud(client):
    token = register(client)

    r = client.get("/users/me", headers=auth_headers(token))
    assert r.status_code == 200

    r = client.post("/exercises", headers=auth_headers(token), json={
        "name":"Bench Press","muscle_group":"Chest","equipment":"Barbell"
    })
    assert r.status_code == 200
    ex_id = r.json()["id"]

    r = client.get("/exercises", headers=auth_headers(token))
    assert r.status_code == 200 and len(r.json()) >= 1

    r = client.get(f"/exercises/{ex_id}", headers=auth_headers(token))
    assert r.status_code == 200 and r.json()["name"] == "Bench Press"

    r = client.put(f"/exercises/{ex_id}", headers=auth_headers(token), json={
        "name":"Incline Bench Press","muscle_group":"Chest","equipment":"Barbell"
    })
    assert r.status_code == 200 and r.json()["name"].startswith("Incline")

    r = client.delete(f"/exercises/{ex_id}", headers=auth_headers(token))
    assert r.status_code == 200 and r.json()["ok"] is True

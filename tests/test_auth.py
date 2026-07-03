def test_register_success(client):
    response = client.post("/auth/register", json={
        "email": "alice@example.com",
        "password": "password123",
        "nom": "Alice",
        "type": "freelance",
    })
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "alice@example.com"
    assert "password" not in data
    assert "password_hash" not in data


def test_register_duplicate_email(client):
    client.post("/auth/register", json={
        "email": "bob@example.com",
        "password": "password123",
        "nom": "Bob",
        "type": "freelance",
    })
    response = client.post("/auth/register", json={
        "email": "bob@example.com",
        "password": "autremotdepasse",
        "nom": "Bob2",
        "type": "client",
    })
    assert response.status_code == 400


def test_login_success(client):
    client.post("/auth/register", json={
        "email": "carla@example.com",
        "password": "password123",
        "nom": "Carla",
        "type": "freelance",
    })
    response = client.post("/auth/login", json={
        "email": "carla@example.com",
        "password": "password123",
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password(client):
    client.post("/auth/register", json={
        "email": "dave@example.com",
        "password": "password123",
        "nom": "Dave",
        "type": "freelance",
    })
    response = client.post("/auth/login", json={
        "email": "dave@example.com",
        "password": "mauvais_mot_de_passe",
    })
    assert response.status_code == 401


def test_me_without_token(client):
    response = client.get("/auth/me")
    assert response.status_code == 401
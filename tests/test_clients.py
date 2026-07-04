def register_and_login(client, email, password="password123"):
    client.post("/auth/register", json={
        "email": email,
        "password": password,
        "nom": "Test User",
        "type": "freelance",
    })
    response = client.post("/auth/login", json={
        "email": email,
        "password": password,
    })
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_create_client_success(client):
    headers = register_and_login(client, "freelance1@example.com")

    response = client.post("/clients/", json={
        "nom": "Entreprise Alpha",
        "email": "contact@alpha.com",
    }, headers=headers)

    assert response.status_code == 201
    data = response.json()
    assert data["nom"] == "Entreprise Alpha"
    assert data["user_id"] is None


def test_create_client_without_token(client):
    response = client.post("/clients/", json={
        "nom": "Entreprise Beta",
        "email": "contact@beta.com",
    })
    assert response.status_code == 401


def test_list_clients_returns_own_clients(client):
    headers = register_and_login(client, "freelance2@example.com")

    client.post("/clients/", json={
        "nom": "Client A",
        "email": "a@example.com",
    }, headers=headers)

    response = client.get("/clients/", headers=headers)

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["nom"] == "Client A"


def test_isolation_between_freelances(client):
    headers_1 = register_and_login(client, "freelance3@example.com")
    headers_2 = register_and_login(client, "freelance4@example.com")


def test_get_client_by_id_success(client):
    headers = register_and_login(client, "freelance15@example.com")

    create_response = client.post("/clients/", json={
        "nom": "Client Detail",
        "email": "detail@example.com",
    }, headers=headers)
    client_id = create_response.json()["id"]

    response = client.get(f"/clients/{client_id}", headers=headers)

    assert response.status_code == 200
    assert response.json()["nom"] == "Client Detail"


def test_get_client_by_id_isolation(client):
    headers_1 = register_and_login(client, "freelance16@example.com")
    headers_2 = register_and_login(client, "freelance17@example.com")

    create_response = client.post("/clients/", json={
        "nom": "Client Prive Detail",
        "email": "privedetail@example.com",
    }, headers=headers_1)
    client_id = create_response.json()["id"]

    response = client.get(f"/clients/{client_id}", headers=headers_2)

    assert response.status_code == 404


def test_client_auto_attachment_on_register(client):
    headers = register_and_login(client, "freelance18@example.com")

    client.post("/clients/", json={
        "nom": "Futur Client",
        "email": "futurclient@example.com",
    }, headers=headers)

    client.post("/auth/register", json={
        "email": "futurclient@example.com",
        "password": "password123",
        "nom": "Futur Client User",
        "type": "client",
    })

    response = client.get("/clients/", headers=headers)
    clients = response.json()
    matching = [c for c in clients if c["email"] == "futurclient@example.com"]

    assert len(matching) == 1
    assert matching[0]["user_id"] is not None    
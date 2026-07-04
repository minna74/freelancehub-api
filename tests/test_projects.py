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


def test_create_project_success(client):
    headers = register_and_login(client, "freelance5@example.com")

    client_response = client.post("/clients/", json={
        "nom": "Client Test",
        "email": "clienttest@example.com",
    }, headers=headers)
    client_id = client_response.json()["id"]

    response = client.post("/projects/", json={
        "nom": "Site vitrine",
        "client_id": client_id,
    }, headers=headers)

    assert response.status_code == 201
    data = response.json()
    assert data["nom"] == "Site vitrine"
    assert data["statut"] == "actif"


def test_create_project_on_someone_elses_client_fails(client):
    headers_1 = register_and_login(client, "freelance6@example.com")
    headers_2 = register_and_login(client, "freelance7@example.com")

    client_response = client.post("/clients/", json={
        "nom": "Client Prive",
        "email": "prive2@example.com",
    }, headers=headers_1)
    client_id = client_response.json()["id"]

    response = client.post("/projects/", json={
        "nom": "Tentative frauduleuse",
        "client_id": client_id,
    }, headers=headers_2)

    assert response.status_code == 404


def test_list_projects_isolation(client):
    headers_1 = register_and_login(client, "freelance8@example.com")
    headers_2 = register_and_login(client, "freelance9@example.com")

    client_response = client.post("/clients/", json={
        "nom": "Client A",
        "email": "a2@example.com",
    }, headers=headers_1)
    client_id = client_response.json()["id"]

    client.post("/projects/", json={
        "nom": "Projet Prive",
        "client_id": client_id,
    }, headers=headers_1)

    response = client.get("/projects/", headers=headers_2)

    assert response.status_code == 200
    assert response.json() == []

def test_client_sees_only_own_projects(client):
    freelance_headers = register_and_login(client, "freelance19@example.com")

    client_response = client.post("/clients/", json={
        "nom": "Client Lecture Seule",
        "email": "lectureseule@example.com",
    }, headers=freelance_headers)

    client.post("/projects/", json={
        "nom": "Projet Visible",
        "client_id": client_response.json()["id"],
    }, headers=freelance_headers)

    client.post("/auth/register", json={
        "email": "lectureseule@example.com",
        "password": "password123",
        "nom": "Client User",
        "type": "client",
    })
    login_response = client.post("/auth/login", json={
        "email": "lectureseule@example.com",
        "password": "password123",
    })
    client_headers = {"Authorization": f"Bearer {login_response.json()['access_token']}"}

    response = client.get("/projects/", headers=client_headers)

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["nom"] == "Projet Visible"
    
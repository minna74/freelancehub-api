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


def create_client_and_project(client, headers):
    client_response = client.post("/clients/", json={
        "nom": "Client Test",
        "email": "clienttask@example.com",
    }, headers=headers)
    client_id = client_response.json()["id"]

    project_response = client.post("/projects/", json={
        "nom": "Projet Test",
        "client_id": client_id,
    }, headers=headers)
    return project_response.json()["id"]


def test_create_task_success(client):
    headers = register_and_login(client, "freelance10@example.com")
    project_id = create_client_and_project(client, headers)

    response = client.post("/tasks/", json={
        "titre": "Configurer le serveur",
        "project_id": project_id,
    }, headers=headers)

    assert response.status_code == 201
    data = response.json()
    assert data["titre"] == "Configurer le serveur"
    assert data["statut"] == "a_faire"
    assert data["priorite"] == "moyenne"


def test_create_task_on_someone_elses_project_fails(client):
    headers_1 = register_and_login(client, "freelance11@example.com")
    headers_2 = register_and_login(client, "freelance12@example.com")

    project_id = create_client_and_project(client, headers_1)

    response = client.post("/tasks/", json={
        "titre": "Tentative frauduleuse",
        "project_id": project_id,
    }, headers=headers_2)

    assert response.status_code == 404


def test_list_tasks_isolation(client):
    headers_1 = register_and_login(client, "freelance13@example.com")
    headers_2 = register_and_login(client, "freelance14@example.com")

    project_id = create_client_and_project(client, headers_1)

    client.post("/tasks/", json={
        "titre": "Tache privee",
        "project_id": project_id,
    }, headers=headers_1)

    response = client.get("/tasks/", headers=headers_2)

    assert response.status_code == 200
    assert response.json() == []


def test_get_task_by_id_success(client):
    headers = register_and_login(client, "freelance27@example.com")
    project_id = create_client_and_project(client, headers)

    task_response = client.post("/tasks/", json={
        "titre": "Tache Detail",
        "project_id": project_id,
    }, headers=headers)
    task_id = task_response.json()["id"]

    response = client.get(f"/tasks/{task_id}", headers=headers)

    assert response.status_code == 200
    assert response.json()["titre"] == "Tache Detail"


def test_get_task_by_id_isolation(client):
    headers_1 = register_and_login(client, "freelance28@example.com")
    headers_2 = register_and_login(client, "freelance29@example.com")
    project_id = create_client_and_project(client, headers_1)

    task_response = client.post("/tasks/", json={
        "titre": "Tache Privee Detail",
        "project_id": project_id,
    }, headers=headers_1)
    task_id = task_response.json()["id"]

    response = client.get(f"/tasks/{task_id}", headers=headers_2)

    assert response.status_code == 404


def test_update_task_success(client):
    headers = register_and_login(client, "freelance30@example.com")
    project_id = create_client_and_project(client, headers)

    task_response = client.post("/tasks/", json={
        "titre": "Titre Original",
        "project_id": project_id,
    }, headers=headers)
    task_id = task_response.json()["id"]

    response = client.patch(f"/tasks/{task_id}", json={
        "titre": "Titre Modifie",
        "project_id": project_id,
        "priorite": "haute",
    }, headers=headers)

    assert response.status_code == 200
    data = response.json()
    assert data["titre"] == "Titre Modifie"
    assert data["priorite"] == "haute"


def test_update_task_forbidden_for_other_freelance(client):
    headers_1 = register_and_login(client, "freelance31@example.com")
    headers_2 = register_and_login(client, "freelance32@example.com")
    project_id = create_client_and_project(client, headers_1)

    task_response = client.post("/tasks/", json={
        "titre": "Tache X",
        "project_id": project_id,
    }, headers=headers_1)
    task_id = task_response.json()["id"]

    response = client.patch(f"/tasks/{task_id}", json={
        "titre": "Tentative Modif",
        "project_id": project_id,
    }, headers=headers_2)

    assert response.status_code == 404


def test_delete_task_success(client):
    headers = register_and_login(client, "freelance33@example.com")
    project_id = create_client_and_project(client, headers)

    task_response = client.post("/tasks/", json={
        "titre": "Tache A Supprimer",
        "project_id": project_id,
    }, headers=headers)
    task_id = task_response.json()["id"]

    delete_response = client.delete(f"/tasks/{task_id}", headers=headers)
    assert delete_response.status_code == 204

    get_response = client.get(f"/tasks/{task_id}", headers=headers)
    assert get_response.status_code == 404


def test_filter_tasks_by_statut(client):
    headers = register_and_login(client, "freelance34@example.com")
    project_id = create_client_and_project(client, headers)

    client.post("/tasks/", json={
        "titre": "Tache A Faire",
        "project_id": project_id,
    }, headers=headers)

    response = client.get("/tasks/?statut=a_faire", headers=headers)

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert all(t["statut"] == "a_faire" for t in data)
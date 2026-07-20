def test_create_project(client, auth_headers):
    response = client.post(
        "/api/projects",
        json={"name": "Test Project", "description": "A test project"},
        headers=auth_headers,
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Project"
    assert data["description"] == "A test project"
    assert "id" in data
    assert "owner_id" in data


def test_create_project_no_name(client, auth_headers):
    response = client.post("/api/projects", json={"description": "No name"}, headers=auth_headers)
    assert response.status_code == 422


def test_list_projects(client, auth_headers):
    client.post("/api/projects", json={"name": "Project 1"}, headers=auth_headers)
    client.post("/api/projects", json={"name": "Project 2"}, headers=auth_headers)
    response = client.get("/api/projects", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2


def test_list_projects_isolation(client, auth_headers):
    client.post("/api/projects", json={"name": "My Project"}, headers=auth_headers)
    other_response = client.post(
        "/api/auth/register", json={"email": "other@example.com", "password": "password123"}
    )
    other_login = client.post(
        "/api/auth/login", json={"email": "other@example.com", "password": "password123"}
    )
    other_headers = {"Authorization": f"Bearer {other_login.json()['access_token']}"}
    other_response = client.get("/api/projects", headers=other_headers)
    assert other_response.status_code == 200
    assert len(other_response.json()) == 0


def test_get_project(client, auth_headers):
    create_resp = client.post("/api/projects", json={"name": "Test"}, headers=auth_headers)
    project_id = create_resp.json()["id"]
    response = client.get(f"/api/projects/{project_id}", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["name"] == "Test"


def test_get_project_not_found(client, auth_headers):
    response = client.get("/api/projects/nonexistent", headers=auth_headers)
    assert response.status_code == 404


def test_update_project(client, auth_headers):
    create_resp = client.post("/api/projects", json={"name": "Old Name"}, headers=auth_headers)
    project_id = create_resp.json()["id"]
    response = client.put(
        f"/api/projects/{project_id}",
        json={"name": "New Name"},
        headers=auth_headers,
    )
    assert response.status_code == 200
    assert response.json()["name"] == "New Name"


def test_delete_project(client, auth_headers):
    create_resp = client.post("/api/projects", json={"name": "To Delete"}, headers=auth_headers)
    project_id = create_resp.json()["id"]
    response = client.delete(f"/api/projects/{project_id}", headers=auth_headers)
    assert response.status_code == 204
    get_resp = client.get(f"/api/projects/{project_id}", headers=auth_headers)
    assert get_resp.status_code == 404


def test_delete_project_cascade(client, auth_headers):
    create_resp = client.post("/api/projects", json={"name": "With Tasks"}, headers=auth_headers)
    project_id = create_resp.json()["id"]
    client.post(
        f"/api/projects/{project_id}/tasks",
        json={"title": "Task 1"},
        headers=auth_headers,
    )
    client.delete(f"/api/projects/{project_id}", headers=auth_headers)
    tasks_resp = client.get(f"/api/projects/{project_id}/tasks", headers=auth_headers)
    assert tasks_resp.status_code == 404

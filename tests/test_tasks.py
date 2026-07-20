def test_create_task(client, auth_headers):
    project_resp = client.post("/api/projects", json={"name": "P1"}, headers=auth_headers)
    project_id = project_resp.json()["id"]
    response = client.post(
        f"/api/projects/{project_id}/tasks",
        json={"title": "Test Task", "status": "TODO"},
        headers=auth_headers,
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Task"
    assert data["status"] == "TODO"
    assert data["project_id"] == project_id


def test_create_task_invalid_status(client, auth_headers):
    project_resp = client.post("/api/projects", json={"name": "P1"}, headers=auth_headers)
    project_id = project_resp.json()["id"]
    response = client.post(
        f"/api/projects/{project_id}/tasks",
        json={"title": "Task", "status": "INVALID"},
        headers=auth_headers,
    )
    assert response.status_code == 422


def test_create_task_project_not_found(client, auth_headers):
    response = client.post(
        "/api/projects/nonexistent/tasks",
        json={"title": "Task"},
        headers=auth_headers,
    )
    assert response.status_code == 404


def test_list_tasks(client, auth_headers):
    project_resp = client.post("/api/projects", json={"name": "P1"}, headers=auth_headers)
    project_id = project_resp.json()["id"]
    client.post(f"/api/projects/{project_id}/tasks", json={"title": "T1"}, headers=auth_headers)
    client.post(f"/api/projects/{project_id}/tasks", json={"title": "T2"}, headers=auth_headers)
    response = client.get(f"/api/projects/{project_id}/tasks", headers=auth_headers)
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_list_tasks_not_found(client, auth_headers):
    response = client.get("/api/projects/nonexistent/tasks", headers=auth_headers)
    assert response.status_code == 404


def test_get_task(client, auth_headers):
    project_resp = client.post("/api/projects", json={"name": "P1"}, headers=auth_headers)
    project_id = project_resp.json()["id"]
    task_resp = client.post(f"/api/projects/{project_id}/tasks", json={"title": "T1"}, headers=auth_headers)
    task_id = task_resp.json()["id"]
    response = client.get(f"/api/tasks/{task_id}", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["title"] == "T1"


def test_update_task(client, auth_headers):
    project_resp = client.post("/api/projects", json={"name": "P1"}, headers=auth_headers)
    project_id = project_resp.json()["id"]
    task_resp = client.post(f"/api/projects/{project_id}/tasks", json={"title": "Old"}, headers=auth_headers)
    task_id = task_resp.json()["id"]
    response = client.put(
        f"/api/tasks/{task_id}",
        json={"title": "New", "status": "IN_PROGRESS"},
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "New"
    assert data["status"] == "IN_PROGRESS"


def test_delete_task(client, auth_headers):
    project_resp = client.post("/api/projects", json={"name": "P1"}, headers=auth_headers)
    project_id = project_resp.json()["id"]
    task_resp = client.post(f"/api/projects/{project_id}/tasks", json={"title": "T1"}, headers=auth_headers)
    task_id = task_resp.json()["id"]
    response = client.delete(f"/api/tasks/{task_id}", headers=auth_headers)
    assert response.status_code == 204


def test_task_ownership_enforced(client, auth_headers):
    project_resp = client.post("/api/projects", json={"name": "P1"}, headers=auth_headers)
    project_id = project_resp.json()["id"]
    task_resp = client.post(f"/api/projects/{project_id}/tasks", json={"title": "T1"}, headers=auth_headers)
    task_id = task_resp.json()["id"]

    client.post("/api/auth/register", json={"email": "other@example.com", "password": "password123"})
    other_login = client.post("/api/auth/login", json={"email": "other@example.com", "password": "password123"})
    other_headers = {"Authorization": f"Bearer {other_login.json()['access_token']}"}

    response = client.get(f"/api/tasks/{task_id}", headers=other_headers)
    assert response.status_code == 403

    response = client.put(f"/api/tasks/{task_id}", json={"title": "Hacked"}, headers=other_headers)
    assert response.status_code == 403

    response = client.delete(f"/api/tasks/{task_id}", headers=other_headers)
    assert response.status_code == 403

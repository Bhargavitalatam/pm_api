def test_register_success(client):
    response = client.post("/api/auth/register", json={"email": "new@example.com", "password": "password123"})
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "new@example.com"
    assert "id" in data


def test_register_duplicate_email(client, registered_user):
    response = client.post("/api/auth/register", json={"email": "test@example.com", "password": "password123"})
    assert response.status_code == 409


def test_register_invalid_email(client):
    response = client.post("/api/auth/register", json={"email": "not-an-email", "password": "password123"})
    assert response.status_code == 422


def test_register_short_password(client):
    response = client.post("/api/auth/register", json={"email": "test@example.com", "password": "123"})
    assert response.status_code == 422


def test_login_success(client, registered_user):
    response = client.post("/api/auth/login", json={"email": "test@example.com", "password": "testpassword123"})
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password(client, registered_user):
    response = client.post("/api/auth/login", json={"email": "test@example.com", "password": "wrongpassword"})
    assert response.status_code == 401


def test_login_nonexistent_user(client):
    response = client.post("/api/auth/login", json={"email": "nonexistent@example.com", "password": "password123"})
    assert response.status_code == 401


def test_get_profile(client, auth_headers):
    response = client.get("/api/users/me", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"
    assert "password_hash" not in data


def test_get_profile_no_auth(client):
    response = client.get("/api/users/me")
    assert response.status_code in (401, 403)

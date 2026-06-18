import uuid


def test_register(client):

    username = f"teste_{uuid.uuid4()}"

    response = client.post(
        "/auth/register", json={"username": username, "password": "12345"}
    )

    assert response.status_code == 201


def test_login(client):

    username = f"teste_{uuid.uuid4()}"

    client.post("/auth/register", json={"username": username, "password": "12345"})

    response = client.post(
        "/auth/login", json={"username": username, "password": "12345"}
    )

    data = response.get_json()

    assert response.status_code == 200

    assert "access_token" in data
    assert "refresh_token" in data


def test_profile(client):

    username = f"teste_{uuid.uuid4()}"

    # Registro
    client.post("/auth/register", json={"username": username, "password": "12345"})

    # Login
    login_response = client.post(
        "/auth/login", json={"username": username, "password": "12345"}
    )

    token = login_response.get_json()["access_token"]

    # Requisição autenticada
    response = client.get("/auth/profile", headers={"Authorization": f"Bearer {token}"})

    data = response.get_json()

    assert response.status_code == 200

    assert data["username"] == username


def test_profile_without_token(client):

    response = client.get("/auth/profile")

    assert response.status_code == 401


def test_profile_invalid_token(client):

    response = client.get(
        "/auth/profile", headers={"Authorization": "Bearer token_fake"}
    )

    assert response.status_code in [401, 422]


def test_refresh_token(client):

    username = f"teste_refresh_{uuid.uuid4()}"

    client.post("/auth/register", json={"username": username, "password": "12345"})

    login_response = client.post(
        "/auth/login", json={"username": username, "password": "12345"}
    )

    assert login_response.status_code == 200

    data = login_response.get_json()

    assert "refresh_token" in data

    refresh_token = data["refresh_token"]

    response = client.post(
        "/auth/refresh", headers={"Authorization": f"Bearer {refresh_token}"}
    )

    data = response.get_json()

    assert response.status_code == 200

    assert "access_token" in data

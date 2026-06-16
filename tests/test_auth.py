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

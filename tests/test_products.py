import uuid


def create_user_and_login(client, role="USER"):

    username = f"user_{uuid.uuid4()}"

    client.post(
        "/auth/register",
        json={"username": username, "password": "12345", "role": role},
    )

    response = client.post(
        "/auth/login", json={"username": username, "password": "12345"}
    )

    return response.get_json()["access_token"]


def test_user_cannot_create_product(client):

    token = create_user_and_login(client, role="USER")

    response = client.post(
        "/products",
        json={"name": "Camisa Barcelona", "price": 99.99, "stock": 10},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 403


def test_admin_can_create_product(client):

    token = create_user_and_login(client, role="ADMIN")

    response = client.post(
        "/products",
        json={"name": "Camisa Real Madrid", "price": 199.99, "stock": 20},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 201

    data = response.get_json()

    assert "id" in data

    assert data["name"] == "Camisa Real Madrid"


def test_admin_can_update_product(client):

    token = create_user_and_login(client, role="ADMIN")

    response = client.post(
        "/products",
        json={"name": "Camisa Arsenal", "price": 149.99, "stock": 15},
        headers={"Authorization": f"Bearer {token}"},
    )

    product_id = response.get_json()["id"]

    response = client.put(
        f"/products/{product_id}",
        json={"name": "Camisa Milan"},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200

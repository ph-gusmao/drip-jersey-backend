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


def test_user_cannot_update_product(client):

    token = create_user_and_login(client, role="ADMIN")

    response = client.post(
        "/products",
        json={"name": "Camisa PSG", "price": 179.99, "stock": 5},
        headers={"Authorization": f"Bearer {token}"},
    )

    product_id = response.get_json()["id"]

    user_token = create_user_and_login(client, role="USER")

    response = client.put(
        f"/products/{product_id}",
        json={"name": "Tentativa de alteração"},
        headers={"Authorization": f"Bearer {user_token}"},
    )

    assert response.status_code == 403


def test_admin_can_delete_product(client):

    token = create_user_and_login(client, role="ADMIN")

    create_response = client.post(
        "/products",
        json={"name": "Camisa Inter", "price": 59.99, "stock": 5},
        headers={"Authorization": f"Bearer {token}"},
    )

    product_id = create_response.get_json()["id"]

    response = client.delete(
        f"/products/{product_id}", headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200


def test_user_cannot_delete_product(client):

    admin_token = create_user_and_login(client, role="ADMIN")

    create_response = client.post(
        "/products",
        json={"name": "Camisa Arsenal", "price": "180", "stock": 3},
        headers={"Authorization": f"Bearer {admin_token}"},
    )

    product_id = create_response.get_json()["id"]

    user_token = create_user_and_login(client, role="USER")

    response = client.delete(
        f"/products/{product_id}", headers={"Authorization": f"Bearer {user_token}"}
    )

    assert response.status_code == 403


def test_get_nonexistent_product(client):

    admin_token = create_user_and_login(client, role="ADMIN")

    response = client.get(
        "/products/999999", headers={"Authorization": f"Bearer {admin_token}"}
    )

    assert response.status_code == 404

    data = response.get_json()

    assert "error" in data


def test_update_nonexistent_product(client):

    admin_token = create_user_and_login(client, role="ADMIN")

    response = client.get(
        "/products/99999",
        json={"name": "Novo nome"},
        headers={"Authorization": f"Bearer {admin_token}"},
    )

    assert response.status_code == 404


def test_delete_nonexistent_product(client):

    admin_token = create_user_and_login(client, role="ADMIN")

    response = client.get(
        "/products/99999", headers={"Authorization": f"Bearer {admin_token}"}
    )

    assert response.status_code == 404


def test_create_product_without_token(client):

    response = client.post(
        "/products", json={"name": "Camisa nike", "price": 149.99, "stock": 10}
    )

    assert response.status_code == 401


def test_create_product_invalid_token(client):

    response = client.post(
        "/products",
        json={"name": "Novo nome", "price": 99, "stock": 10},
        headers={"Authorization": "Bearer invalid_token"},
    )

    assert response.status_code == 422


def test_register_duplicate_user(client):

    username = "usuario_duplicado"

    client.post("/auth/register", json={"username": username, "password": "12345"})

    response = client.post(
        "/auth/register", json={"username": username, "password": "12345"}
    )

    assert response.status_code == 400


def test_login_wrong_password(client):

    username = "usuario_login"

    client.post("/auth/register", json={"username": username, "password": "12345"})

    response = client.post(
        "/auth/login", json={"username": username, "password": "wrong_password"}
    )

    assert response.status_code == 401

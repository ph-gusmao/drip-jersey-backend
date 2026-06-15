def test_register(client):

    response = client.post(
        "/auth/register", json={"username": "teste", "password": "12345"}
    )

    data = response.get_json()

    assert response.status_code == 201

    assert "id" in data

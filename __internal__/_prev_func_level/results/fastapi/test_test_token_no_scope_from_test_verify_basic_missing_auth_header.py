def test_token_inactive_user_with_no_scope(client: TestClient):
    access_token = get_access_token(username="inactive_user", password="secret", scope=None, client=client)
    response = client.get(
        "/users/me", headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 400, response.text
    assert response.json() == {"detail": "Inactive user"}
    assert response.headers["WWW-Authenticate"] == 'Bearer scope="me"'

def test_token_with_invalid_username(client: TestClient):
    access_token = get_access_token(username="invalid_user", password="wrong_password", scope=None, client=client)
    response = client.get(
        "/users/me", headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 401, response.text
    assert response.json() == {"detail": "Could not validate credentials"}
    assert response.headers["WWW-Authenticate"] == 'Bearer scope="me"'

def test_token_with_empty_username(client: TestClient):
    access_token = get_access_token(username="", password="secret", scope=None, client=client)
    response = client.get(
        "/users/me", headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 401, response.text
    assert response.json() == {"detail": "Could not validate credentials"}
    assert response.headers["WWW-Authenticate"] == 'Bearer scope="me"'

def test_token_with_empty_password(client: TestClient):
    access_token = get_access_token(username="johndoe", password="", scope=None, client=client)
    response = client.get(
        "/users/me", headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 401, response.text
    assert response.json() == {"detail": "Could not validate credentials"}
    assert response.headers["WWW-Authenticate"] == 'Bearer scope="me"'

def test_token_with_special_characters_in_username(client: TestClient):
    access_token = get_access_token(username="john@doe", password="secret", scope=None, client=client)
    response = client.get(
        "/users/me", headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 401, response.text
    assert response.json() == {"detail": "Not enough permissions"}
    assert response.headers["WWW-Authenticate"] == 'Bearer scope="me"'
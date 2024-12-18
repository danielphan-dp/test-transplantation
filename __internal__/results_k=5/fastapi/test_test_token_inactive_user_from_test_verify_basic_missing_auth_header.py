import pytest
from fastapi.testclient import TestClient
from utils.needs_py39 import needs_py39
from docs_src.security.tutorial005_an_py39.app import get_access_token

@needs_py39
def test_token_inactive_user_with_different_username(client: TestClient):
    access_token = get_access_token(
        username="bob", password="secretbob", scope="me", client=client
    )
    response = client.get(
        "/users/me", headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 400, response.text
    assert response.json() == {"detail": "Inactive user"}

@needs_py39
def test_token_with_invalid_scope(client: TestClient):
    access_token = get_access_token(
        username="johndoe", password="secret", scope="invalid_scope", client=client
    )
    response = client.get(
        "/users/me", headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 401, response.text
    assert response.json() == {"detail": "Not enough permissions"}

@needs_py39
def test_token_with_empty_scope(client: TestClient):
    access_token = get_access_token(
        username="johndoe", password="secret", scope="", client=client
    )
    response = client.get(
        "/users/me", headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 401, response.text
    assert response.json() == {"detail": "Not enough permissions"}

@needs_py39
def test_token_with_nonexistent_user(client: TestClient):
    access_token = get_access_token(
        username="nonexistent", password="wrongpassword", scope="me", client=client
    )
    response = client.get(
        "/users/me", headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 401, response.text
    assert response.json() == {"detail": "Could not validate credentials"}

@needs_py39
def test_token_with_missing_password(client: TestClient):
    access_token = get_access_token(
        username="johndoe", password="", scope="me", client=client
    )
    response = client.get(
        "/users/me", headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 401, response.text
    assert response.json() == {"detail": "Could not validate credentials"}
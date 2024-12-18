import pytest
from fastapi.testclient import TestClient
from utils.needs_py310 import needs_py310
from docs_src.security.tutorial005_an_py310.app import get_access_token

@needs_py310
def test_get_access_token_no_scope(client: TestClient):
    access_token = get_access_token(client=client)
    response = client.get("/users/me", headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 200, response.text
    assert response.json() == {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "disabled": False,
    }

@needs_py310
def test_get_access_token_invalid_credentials(client: TestClient):
    access_token = get_access_token(username="invaliduser", password="wrongpassword", client=client)
    assert access_token is None

@needs_py310
def test_get_access_token_empty_username(client: TestClient):
    access_token = get_access_token(username="", password="secret", client=client)
    assert access_token is None

@needs_py310
def test_get_access_token_empty_password(client: TestClient):
    access_token = get_access_token(username="johndoe", password="", client=client)
    assert access_token is None

@needs_py310
def test_get_access_token_with_scope(client: TestClient):
    access_token = get_access_token(scope="admin", client=client)
    response = client.get("/users/me", headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 200, response.text
    assert response.json() == {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "disabled": False,
    }

@needs_py310
def test_get_access_token_invalid_scope(client: TestClient):
    access_token = get_access_token(scope="invalid_scope", client=client)
    response = client.get("/users/me", headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 403, response.text
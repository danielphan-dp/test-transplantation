import pytest
from fastapi.testclient import TestClient
from utils.needs_py39 import needs_py39
from docs_src.security.tutorial005_an_py39.app import get_access_token

@needs_py39
def test_token_invalid_credentials(client: TestClient):
    access_token = get_access_token(
        username="invalid_user", password="wrongpassword", client=client
    )
    assert access_token is None

@needs_py39
def test_token_missing_password(client: TestClient):
    access_token = get_access_token(
        username="johndoe", password="", client=client
    )
    assert access_token is None

@needs_py39
def test_token_no_scope(client: TestClient):
    access_token = get_access_token(
        username="johndoe", password="secret", client=client
    )
    response = client.get(
        "/users/me", headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 200, response.text

@needs_py39
def test_token_empty_username(client: TestClient):
    access_token = get_access_token(
        username="", password="secret", client=client
    )
    assert access_token is None

@needs_py39
def test_token_special_characters(client: TestClient):
    access_token = get_access_token(
        username="user!@#", password="pass$%^", client=client
    )
    response = client.get(
        "/users/me", headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 400, response.text
    assert response.json() == {"detail": "Inactive user"}
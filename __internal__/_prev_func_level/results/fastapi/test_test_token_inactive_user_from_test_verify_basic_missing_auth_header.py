import pytest
from fastapi.testclient import TestClient
from utils.needs_py39 import needs_py39
from docs_src.security.tutorial005_an_py39.app import get_access_token

@needs_py39
def test_token_no_password(client: TestClient):
    response = client.post("/token", data={"username": "johndoe"})
    assert response.status_code == 400, response.text
    assert response.json() == {"detail": "Missing password"}

@needs_py39
def test_token_no_username(client: TestClient):
    response = client.post("/token", data={"password": "secret"})
    assert response.status_code == 400, response.text
    assert response.json() == {"detail": "Missing username"}

@needs_py39
def test_token_invalid_credentials(client: TestClient):
    access_token = get_access_token(username="invaliduser", password="wrongpassword", scope="me", client=client)
    response = client.get("/users/me", headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 401, response.text
    assert response.json() == {"detail": "Could not validate credentials"}

@needs_py39
def test_token_no_scope(client: TestClient):
    access_token = get_access_token(username="johndoe", password="secret", client=client)
    response = client.get("/users/me", headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 401, response.text
    assert response.json() == {"detail": "Not enough permissions"}

@needs_py39
def test_token_inactive_user_with_invalid_scope(client: TestClient):
    access_token = get_access_token(username="alice", password="secretalice", scope="invalidscope", client=client)
    response = client.get("/users/me", headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 400, response.text
    assert response.json() == {"detail": "Inactive user"}
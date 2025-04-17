import pytest
from fastapi.testclient import TestClient
from utils.needs_py310 import needs_py310
from docs_src.security.tutorial005_an_py310.app import get_access_token

@needs_py310
def test_token_incorrect_password(client: TestClient):
    access_token = get_access_token(username="johndoe", password="wrongpassword", scope="me", client=client)
    response = client.get("/users/me", headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 401, response.text
    assert response.json() == {"detail": "Could not validate credentials"}

@needs_py310
def test_token_no_username(client: TestClient):
    access_token = get_access_token(username="", password="secret", scope="me", client=client)
    response = client.get("/users/me", headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 401, response.text
    assert response.json() == {"detail": "Could not validate credentials"}

@needs_py310
def test_token_no_scope(client: TestClient):
    access_token = get_access_token(client=client)
    response = client.get("/users/me", headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 401, response.text
    assert response.json() == {"detail": "Not enough permissions"}

@needs_py310
def test_token_inactive_user(client: TestClient):
    access_token = get_access_token(username="alice", password="secretalice", scope="me", client=client)
    response = client.get("/users/me", headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 400, response.text
    assert response.json() == {"detail": "Inactive user"}

@needs_py310
def test_token_nonexistent_user(client: TestClient):
    access_token = get_access_token(username="nonexistent", password="secret", scope="me", client=client)
    response = client.get("/users/me", headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 401, response.text
    assert response.json() == {"detail": "Could not validate credentials"}

@needs_py310
def test_read_items_with_scope(client: TestClient):
    access_token = get_access_token(scope="me items", client=client)
    response = client.get("/users/me/items/", headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 200, response.text
    assert response.json() == [{"item_id": "Foo", "owner": "johndoe"}]
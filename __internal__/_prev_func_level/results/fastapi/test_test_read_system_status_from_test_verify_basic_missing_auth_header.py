import pytest
from fastapi.testclient import TestClient
from utils.needs_py310 import needs_py310
from docs_src.security.tutorial005_an_py310 import get_access_token

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
def test_get_access_token_incorrect_credentials(client: TestClient):
    access_token = get_access_token(username="wronguser", password="wrongpass", client=client)
    response = client.get("/users/me", headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 401, response.text
    assert response.json() == {"detail": "Could not validate credentials"}

@needs_py310
def test_get_access_token_no_username(client: TestClient):
    response = client.post("/token", data={'password': 'secret'})
    assert response.status_code == 422, response.text

@needs_py310
def test_get_access_token_no_password(client: TestClient):
    response = client.post("/token", data={'username': 'johndoe'})
    assert response.status_code == 422, response.text

@needs_py310
def test_get_access_token_invalid_scope(client: TestClient):
    access_token = get_access_token(scope="invalid_scope", client=client)
    response = client.get("/users/me", headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 401, response.text
    assert response.json() == {"detail": "Not enough permissions"}
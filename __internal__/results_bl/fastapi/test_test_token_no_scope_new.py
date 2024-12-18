import pytest
from fastapi.testclient import TestClient
from docs_src.security.tutorial005.app import app

client = TestClient(app)

def test_token_with_invalid_username():
    access_token = get_access_token(username='invaliduser', password='secret', client=client)
    response = client.get("/users/me", headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 401, response.text
    assert response.json() == {"detail": "Not enough permissions"}
    assert response.headers["WWW-Authenticate"] == 'Bearer scope="me"'

def test_token_with_invalid_password():
    access_token = get_access_token(username='johndoe', password='wrongpassword', client=client)
    response = client.get("/users/me", headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 401, response.text
    assert response.json() == {"detail": "Not enough permissions"}
    assert response.headers["WWW-Authenticate"] == 'Bearer scope="me"'

def test_token_with_scope():
    access_token = get_access_token(username='johndoe', password='secret', scope='me', client=client)
    response = client.get("/users/me", headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 200, response.text
    assert 'username' in response.json()  # Assuming the response contains the username

def test_token_with_empty_username():
    access_token = get_access_token(username='', password='secret', client=client)
    response = client.get("/users/me", headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 401, response.text
    assert response.json() == {"detail": "Not enough permissions"}
    assert response.headers["WWW-Authenticate"] == 'Bearer scope="me"'

def test_token_with_empty_password():
    access_token = get_access_token(username='johndoe', password='', client=client)
    response = client.get("/users/me", headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 401, response.text
    assert response.json() == {"detail": "Not enough permissions"}
    assert response.headers["WWW-Authenticate"] == 'Bearer scope="me"'
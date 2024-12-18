import pytest
from flask import Flask

@pytest.fixture
def app():
    app = Flask(__name__)
    return app

@pytest.fixture
def client(app):
    return app.test_client()

def test_post_create(client):
    response = client.post("/")
    assert response.data == b"Create"
    assert response.status_code == 200

def test_post_method_not_allowed(client):
    response = client.get("/")
    assert response.status_code == 405
    assert sorted(response.allow) == ["POST"]

def test_post_with_invalid_data(client):
    response = client.post("/", json={"invalid": "data"})
    assert response.status_code == 400  # Assuming the method should return 400 for invalid data

def test_post_with_missing_body(client):
    response = client.post("/", data={})
    assert response.status_code == 400  # Assuming the method should return 400 for missing body

def test_post_options_method(client):
    response = client.open("/", method="OPTIONS")
    assert response.status_code == 200
    assert sorted(response.allow) == ["POST", "OPTIONS"]  # Assuming OPTIONS should allow POST
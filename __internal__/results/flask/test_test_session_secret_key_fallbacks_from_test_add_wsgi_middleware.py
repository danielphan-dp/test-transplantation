import pytest
from flask import Flask

@pytest.fixture
def app():
    app = Flask(__name__)
    return app

@pytest.fixture
def client(app):
    return app.test_client()

@app.post("/create")
def create_post():
    return 'Create'

def test_create_post(client):
    response = client.post("/create")
    assert response.data.decode() == 'Create'
    assert response.status_code == 200

def test_create_post_invalid_method(client):
    response = client.get("/create")
    assert response.status_code == 405  # Method Not Allowed

def test_create_post_with_data(client):
    response = client.post("/create", data={"title": "Test Title", "body": "Test Body"})
    assert response.data.decode() == 'Create'
    assert response.status_code == 200

def test_create_post_empty_data(client):
    response = client.post("/create", data={})
    assert response.data.decode() == 'Create'
    assert response.status_code == 200

def test_create_post_with_invalid_data(client):
    response = client.post("/create", data={"invalid": "data"})
    assert response.data.decode() == 'Create'
    assert response.status_code == 200
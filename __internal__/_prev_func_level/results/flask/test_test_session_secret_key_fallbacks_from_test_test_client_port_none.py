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
def create():
    return 'Create'

def test_create_endpoint(client):
    response = client.post("/create")
    assert response.data.decode() == 'Create'
    assert response.status_code == 200

def test_create_invalid_method(client):
    response = client.get("/create")
    assert response.status_code == 405

def test_create_with_data(client):
    response = client.post("/create", data={"key": "value"})
    assert response.data.decode() == 'Create'
    assert response.status_code == 200

def test_create_empty_data(client):
    response = client.post("/create", data={})
    assert response.data.decode() == 'Create'
    assert response.status_code == 200
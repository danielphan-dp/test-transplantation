import pytest
from flask import Flask, jsonify

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

def test_create_with_invalid_data(client):
    response = client.post("/create", data={})
    assert response.data.decode() == 'Create'
    assert response.status_code == 200

def test_create_with_additional_data(client):
    response = client.post("/create", data={"extra": "data"})
    assert response.data.decode() == 'Create'
    assert response.status_code == 200

def test_create_endpoint_not_found(client):
    response = client.post("/nonexistent")
    assert response.status_code == 404
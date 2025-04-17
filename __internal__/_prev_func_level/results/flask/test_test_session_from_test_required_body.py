import pytest
from flask import Flask, request

@pytest.fixture
def app():
    app = Flask(__name__)
    return app

@pytest.fixture
def client(app):
    return app.test_client()

@app.route("/create", methods=["POST"])
def create():
    return 'Create'

def test_create_endpoint(client):
    response = client.post("/create")
    assert response.data == b'Create'
    assert response.status_code == 200

def test_create_with_invalid_data(client):
    response = client.post("/create", data={"invalid": "data"})
    assert response.data == b'Create'
    assert response.status_code == 200

def test_create_with_no_data(client):
    response = client.post("/create", data={})
    assert response.data == b'Create'
    assert response.status_code == 200

def test_create_with_json(client):
    response = client.post("/create", json={"key": "value"})
    assert response.data == b'Create'
    assert response.status_code == 200
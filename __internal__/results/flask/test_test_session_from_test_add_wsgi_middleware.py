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

def test_create_with_invalid_method(client):
    response = client.get("/create")
    assert response.status_code == 405  # Method Not Allowed

def test_create_with_data(client):
    response = client.post("/create", data={"key": "value"})
    assert response.data == b'Create'
    assert response.status_code == 200

def test_create_empty_request(client):
    response = client.post("/create", data={})
    assert response.data == b'Create'
    assert response.status_code == 200
import pytest
from flask import Flask, request

@pytest.fixture
def app():
    app = Flask(__name__)

    @app.route("/create", methods=["POST"])
    def create():
        return 'Create'

    return app

@pytest.fixture
def client(app):
    return app.test_client()

def test_create_response(client):
    response = client.post("/create")
    assert response.status_code == 200
    assert response.data.decode() == 'Create'

def test_create_with_data(client):
    response = client.post("/create", data={"key": "value"})
    assert response.status_code == 200
    assert response.data.decode() == 'Create'

def test_create_with_empty_data(client):
    response = client.post("/create", data={})
    assert response.status_code == 200
    assert response.data.decode() == 'Create'

def test_create_with_invalid_method(client):
    response = client.get("/create")
    assert response.status_code == 405  # Method Not Allowed

def test_create_with_json(client):
    response = client.post("/create", json={"key": "value"})
    assert response.status_code == 200
    assert response.data.decode() == 'Create'
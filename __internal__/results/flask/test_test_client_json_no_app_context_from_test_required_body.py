import pytest
from flask import Flask, json

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

def test_create_endpoint(client):
    response = client.post("/create")
    assert response.data.decode() == 'Create'
    assert response.status_code == 200

def test_create_with_json(client):
    response = client.post("/create", json={"data": "test"})
    assert response.data.decode() == 'Create'
    assert response.status_code == 200

def test_create_no_data(client):
    response = client.post("/create", data={})
    assert response.data.decode() == 'Create'
    assert response.status_code == 200

def test_create_invalid_method(client):
    response = client.get("/create")
    assert response.status_code == 405  # Method Not Allowed
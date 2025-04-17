import pytest
from flask import Flask, jsonify, request

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
    assert response.status_code == 200
    assert response.data.decode() == 'Create'

def test_create_with_json(client):
    json_data = {"name": "test"}
    response = client.post("/create", json=json_data)
    assert response.status_code == 200
    assert response.data.decode() == 'Create'

def test_create_no_json(client):
    response = client.post("/create", data="Not JSON")
    assert response.status_code == 200
    assert response.data.decode() == 'Create'

def test_create_empty_json(client):
    response = client.post("/create", json={})
    assert response.status_code == 200
    assert response.data.decode() == 'Create'
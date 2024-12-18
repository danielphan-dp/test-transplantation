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

def test_create_endpoint(client):
    response = client.post("/create")
    assert response.data == b'Create'
    assert response.status_code == 200

def test_create_with_invalid_data(client):
    response = client.post("/create", data=None, content_type="application/json")
    assert response.status_code == 400
    assert b"Failed to decode JSON object" in response.data

@pytest.mark.parametrize("data", [None, "", "invalid_json"])
def test_create_with_various_payloads(client, data):
    response = client.post("/create", data=data, content_type="application/json")
    assert response.status_code == 400
    assert b"Failed to decode JSON object" in response.data

def test_create_with_valid_json(client):
    response = client.post("/create", json={"key": "value"})
    assert response.data == b'Create'
    assert response.status_code == 200
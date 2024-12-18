import pytest
from flask import Flask, jsonify, request

@pytest.fixture
def app():
    app = Flask(__name__)

    @app.route("/create", methods=["POST"])
    def create():
        return 'Create'

    return app

def test_create_valid_request(client):
    response = client.post("/create", json={"title": "Test Title", "body": "Test Body"})
    assert response.data == b'Create'
    assert response.status_code == 200

def test_create_invalid_request(client):
    response = client.post("/create", data="malformed", content_type="application/json")
    assert response.status_code == 400

def test_create_missing_title(client):
    response = client.post("/create", json={"body": "Test Body"})
    assert response.status_code == 400

def test_create_empty_body(client):
    response = client.post("/create", json={"title": "Test Title", "body": ""})
    assert response.status_code == 400

def test_create_no_json(client):
    response = client.post("/create", data="not json", content_type="text/plain")
    assert response.status_code == 400
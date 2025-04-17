import pytest
from flask import Flask, jsonify, request

@pytest.fixture
def app():
    app = Flask(__name__)

    @app.route("/create", methods=["POST"])
    def create():
        return 'Create'

    return app

def test_create_endpoint(client):
    response = client.post("/create")
    assert response.data.decode() == 'Create'
    assert response.status_code == 200

def test_create_with_invalid_data(client):
    response = client.post("/create", data="malformed", content_type="application/json")
    assert response.status_code == 400

def test_create_with_missing_data(client):
    response = client.post("/create", data={}, content_type="application/json")
    assert response.status_code == 400
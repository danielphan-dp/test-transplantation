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
    assert response.data.decode() == 'Create'
    assert response.status_code == 200

def test_create_with_data(client):
    response = client.post("/create", data={"key": "value"})
    assert response.data.decode() == 'Create'
    assert response.status_code == 200

def test_create_no_data(client):
    response = client.post("/create", data={})
    assert response.data.decode() == 'Create'
    assert response.status_code == 200

def test_create_invalid_method(client):
    response = client.get("/create")
    assert response.status_code == 405  # Method Not Allowed

def test_create_with_additional_args(client):
    response = client.post("/create?extra=1", data={"key": "value"})
    assert response.data.decode() == 'Create'
    assert response.status_code == 200
    assert "extra" in request.args
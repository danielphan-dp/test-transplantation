import pytest
from flask import Flask, request

@pytest.fixture
def app():
    app = Flask(__name__)

    @app.route("/create", methods=["POST"])
    def create():
        return 'Create'

    return app

def test_create_method(client):
    response = client.post("/create")
    assert response.data == b'Create'
    assert response.status_code == 200

def test_create_method_invalid_method(client):
    response = client.get("/create")
    assert response.status_code == 405
    assert sorted(response.allow) == ["POST", "HEAD", "OPTIONS"]

def test_create_method_no_data(client):
    response = client.post("/create", data={})
    assert response.data == b'Create'
    assert response.status_code == 200

def test_create_method_with_data(client):
    response = client.post("/create", data={"key": "value"})
    assert response.data == b'Create'
    assert response.status_code == 200

def test_create_method_with_invalid_route(client):
    response = client.post("/nonexistent")
    assert response.status_code == 404
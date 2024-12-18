import pytest
from flask import Flask, request

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

def test_create_with_data(client):
    response = client.post("/create", data={"key": "value"})
    assert response.data.decode() == 'Create'
    assert response.status_code == 200

def test_create_invalid_method(client):
    response = client.get("/create")
    assert response.status_code == 405

def test_create_no_data(client):
    response = client.post("/create", data={})
    assert response.data.decode() == 'Create'
    assert response.status_code == 200
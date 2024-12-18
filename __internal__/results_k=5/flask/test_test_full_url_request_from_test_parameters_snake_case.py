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

def test_create_with_query_params(client):
    response = client.post("/create?param=value")
    assert response.status_code == 200
    assert response.data.decode() == 'Create'
    assert "param" in request.args
    assert request.args["param"] == "value"
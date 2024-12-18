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
    assert response.data == b'Create'

def test_create_with_invalid_method(client):
    response = client.get("/create")
    assert response.status_code == 405

def test_create_with_data(client):
    response = client.post("/create", data={"title": "Test Title"})
    assert response.data == b'Create'  # Assuming the method does not change with data

def test_create_with_empty_data(client):
    response = client.post("/create", data={})
    assert response.data == b'Create'  # Assuming the method does not change with empty data
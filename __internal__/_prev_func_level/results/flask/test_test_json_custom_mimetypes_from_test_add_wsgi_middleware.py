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
    rv = client.post("/create")
    assert rv.data == b'Create'

def test_create_with_invalid_method(client):
    rv = client.get("/create")
    assert rv.status_code == 405

def test_create_with_data(client):
    rv = client.post("/create", data={"key": "value"})
    assert rv.data == b'Create'
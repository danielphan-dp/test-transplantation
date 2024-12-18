import pytest
from flask import Flask, request

@pytest.fixture
def app():
    app = Flask(__name__)

    @app.route("/create", methods=["POST"])
    def create():
        return 'Create'

    return app

def test_create_action(client):
    with client:
        rv = client.post("/create", data={"key": "value"})
        assert rv.status_code == 200
        assert rv.data.decode() == 'Create'

def test_create_action_empty_data(client):
    with client:
        rv = client.post("/create", data={})
        assert rv.status_code == 200
        assert rv.data.decode() == 'Create'

def test_create_action_invalid_method(client):
    with client:
        rv = client.get("/create")
        assert rv.status_code == 405  # Method Not Allowed

def test_create_action_with_query_params(client):
    with client:
        rv = client.post("/create?param=1", data={"key": "value"})
        assert rv.status_code == 200
        assert rv.data.decode() == 'Create'
        assert "param" in request.args
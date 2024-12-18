import pytest
from flask import Flask, request

@pytest.fixture
def app():
    app = Flask(__name__)

    @app.route("/create", methods=["POST"])
    def post():
        return 'Create'

    return app

@pytest.fixture
def client(app):
    return app.test_client()

def test_post_create(client):
    rv = client.post("/create")
    assert rv.status_code == 200
    assert rv.data == b'Create'

def test_post_create_with_json(client):
    rv = client.post("/create", json={"key": "value"})
    assert rv.status_code == 200
    assert rv.data == b'Create'

def test_post_create_with_empty_data(client):
    rv = client.post("/create", data=None)
    assert rv.status_code == 200
    assert rv.data == b'Create'

def test_post_create_with_invalid_json(client):
    rv = client.post("/create", data="invalid json", content_type="application/json")
    assert rv.status_code == 200
    assert rv.data == b'Create'
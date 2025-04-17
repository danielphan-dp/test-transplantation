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
    assert rv.status_code == 200

def test_create_with_invalid_method(client):
    rv = client.get("/create")
    assert rv.status_code == 405

def test_create_with_empty_body(client):
    rv = client.post("/create", data="")
    assert rv.data == b'Create'
    assert rv.status_code == 200

def test_create_with_json_content_type(client):
    rv = client.post("/create", json={"key": "value"}, content_type="application/json")
    assert rv.data == b'Create'
    assert rv.status_code == 200

def test_create_with_custom_mimetype(client):
    rv = client.post("/create", data='"foo"', content_type="application/x+json")
    assert rv.data == b'Create'
    assert rv.status_code == 200
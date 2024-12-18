import pytest
from flask import Flask, json

@pytest.fixture
def app():
    app = Flask(__name__)

    @app.route("/", methods=["POST"])
    def post():
        return 'Create'

    return app

@pytest.fixture
def client(app):
    return app.test_client()

def test_post_create(client):
    rv = client.post("/", json={})
    assert rv.data == b'Create'

def test_post_with_data(client):
    rv = client.post("/", json={"data": "test"})
    assert rv.data == b'Create'

def test_post_empty_json(client):
    rv = client.post("/", json={})
    assert rv.data == b'Create'

def test_post_invalid_method(client):
    rv = client.get("/")
    assert rv.status_code == 405  # Method Not Allowed

def test_post_with_large_payload(client):
    large_payload = {"data": "x" * 10000}
    rv = client.post("/", json=large_payload)
    assert rv.data == b'Create'
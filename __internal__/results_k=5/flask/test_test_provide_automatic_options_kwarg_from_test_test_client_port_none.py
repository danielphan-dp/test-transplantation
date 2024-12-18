import pytest
from flask import Flask, request

@pytest.fixture
def app():
    app = Flask(__name__)

    @app.route("/", methods=["POST"])
    def create():
        return 'Create'

    return app

@pytest.fixture
def client(app):
    return app.test_client()

def test_post_create(client):
    rv = client.post("/")
    assert rv.data == b'Create'
    assert rv.status_code == 200

def test_post_method_not_allowed(client):
    rv = client.get("/")
    assert rv.status_code == 405
    assert sorted(rv.allow) == ["POST"]

def test_post_with_invalid_method(client):
    rv = client.put("/")
    assert rv.status_code == 405
    assert sorted(rv.allow) == ["POST"]
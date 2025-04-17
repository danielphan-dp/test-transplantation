import pytest
from flask import Flask

@pytest.fixture
def app():
    app = Flask(__name__)
    return app

@pytest.fixture
def client(app):
    return app.test_client()

def test_post_create(client):
    rv = client.post("/")
    assert rv.data == b"Create"
    assert rv.status_code == 200

def test_post_method_not_allowed(client):
    rv = client.get("/")
    assert rv.status_code == 405
    assert sorted(rv.allow) == ["POST"]

def test_post_with_options(client):
    rv = client.open("/", method="OPTIONS")
    assert rv.status_code == 200
    assert sorted(rv.allow) == ["POST"]
import pytest
from flask import Flask, json

@pytest.fixture
def app():
    app = Flask(__name__)

    @app.route("/", methods=["POST"])
    def create():
        return 'Create'

    return app

def test_post_create(client):
    rv = client.post("/", json={})
    assert rv.data.decode() == 'Create'
    assert rv.status_code == 200

def test_post_with_data(client):
    rv = client.post("/", json={"data": "test"})
    assert rv.data.decode() == 'Create'
    assert rv.status_code == 200

def test_post_empty_json(client):
    rv = client.post("/", json={})
    assert rv.data.decode() == 'Create'
    assert rv.status_code == 200

def test_post_invalid_method(client):
    rv = client.get("/")
    assert rv.status_code == 405
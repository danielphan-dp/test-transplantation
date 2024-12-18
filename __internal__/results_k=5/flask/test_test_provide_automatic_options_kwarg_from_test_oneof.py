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
    assert rv.status_code == 200
    assert rv.data == b'Create'

def test_post_method_not_allowed(client):
    rv = client.get("/")
    assert rv.status_code == 405
    assert sorted(rv.allow) == ["POST"]

def test_post_with_invalid_data(client):
    rv = client.post("/", json={"invalid": "data"})
    assert rv.status_code == 400  # Assuming the method should return 400 for invalid data

def test_post_with_missing_data(client):
    rv = client.post("/", json={})
    assert rv.status_code == 400  # Assuming the method should return 400 for missing data

def test_post_options_method(client):
    rv = client.open("/", method="OPTIONS")
    assert rv.status_code == 200
    assert sorted(rv.allow) == ["POST", "OPTIONS"]  # Assuming OPTIONS should allow POST
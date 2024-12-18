import pytest
from flask import Flask

@pytest.fixture
def app():
    app = Flask(__name__)
    return app

def test_post_create(app, client):
    response = client.post("/create")
    assert response.data == b'Create'
    assert response.status_code == 200

def test_post_create_with_data(app, client):
    response = client.post("/create", json={"foo": "bar"})
    assert response.data == b'Create'
    assert response.status_code == 200

def test_post_create_no_data(app, client):
    response = client.post("/create", data={})
    assert response.data == b'Create'
    assert response.status_code == 200

def test_post_create_invalid_method(app, client):
    response = client.get("/create")
    assert response.status_code == 405  # Method Not Allowed
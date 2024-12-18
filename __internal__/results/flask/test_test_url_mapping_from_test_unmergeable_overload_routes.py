import pytest
from flask import Flask

@pytest.fixture
def app():
    app = Flask(__name__)
    app.add_url_rule("/", "create", lambda: 'Create', methods=["POST"])
    return app

def test_post_create(client):
    response = client.post("/")
    assert response.data == b'Create'
    assert response.status_code == 200

def test_post_create_invalid_method(client):
    response = client.get("/")
    assert response.status_code == 405
    assert sorted(response.allow) == ["POST"]

def test_post_create_no_data(client):
    response = client.post("/", data={})
    assert response.data == b'Create'
    assert response.status_code == 200

def test_post_create_with_additional_data(client):
    response = client.post("/", data={"extra": "data"})
    assert response.data == b'Create'
    assert response.status_code == 200

def test_post_create_with_invalid_method(client):
    response = client.put("/")
    assert response.status_code == 405
    assert sorted(response.allow) == ["POST"]
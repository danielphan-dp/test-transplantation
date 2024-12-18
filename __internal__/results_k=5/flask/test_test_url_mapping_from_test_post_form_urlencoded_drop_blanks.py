import pytest
from flask import Flask

@pytest.fixture
def app():
    app = Flask(__name__)

    @app.route("/", methods=["POST"])
    def post():
        return 'Create'

    return app

def test_post_create(client):
    response = client.post("/")
    assert response.data == b'Create'
    assert response.status_code == 200

def test_post_invalid_method(client):
    response = client.get("/")
    assert response.status_code == 405
    assert sorted(response.allow) == ["POST", "OPTIONS"]

def test_post_with_data(client):
    response = client.post("/", data={"key": "value"})
    assert response.data == b'Create'
    assert response.status_code == 200

def test_post_empty_data(client):
    response = client.post("/", data={})
    assert response.data == b'Create'
    assert response.status_code == 200

def test_post_invalid_route(client):
    response = client.post("/invalid")
    assert response.status_code == 404
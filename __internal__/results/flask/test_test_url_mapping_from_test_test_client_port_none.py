import pytest
from flask import Flask, request

@pytest.fixture
def app():
    app = Flask(__name__)
    @app.route("/", methods=["POST"])
    def post():
        return 'Create'
    return app

def test_post_method(client):
    response = client.post("/")
    assert response.data == b'Create'
    assert response.status_code == 200

def test_post_method_invalid_method(client):
    response = client.get("/")
    assert response.status_code == 405
    assert sorted(response.allow) == ["GET", "HEAD", "OPTIONS", "POST"]
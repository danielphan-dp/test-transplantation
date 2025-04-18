import pytest
from flask import Flask, request

@pytest.fixture
def app():
    app = Flask(__name__)

    @app.route("/create", methods=["POST"])
    def create():
        return 'Create'

    return app

def test_create_method(client):
    response = client.post("/create")
    assert response.data == b'Create'
    assert response.status_code == 200

def test_create_method_invalid_method(client):
    response = client.get("/create")
    assert response.status_code == 405
    assert sorted(response.allow) == ["POST", "HEAD", "OPTIONS"]
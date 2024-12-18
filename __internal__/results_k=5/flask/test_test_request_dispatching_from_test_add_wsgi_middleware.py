import pytest
from flask import Flask

@pytest.fixture
def app():
    app = Flask(__name__)

    @app.route("/create", methods=["POST"])
    def create():
        return 'Create'

    return app

@pytest.fixture
def client(app):
    return app.test_client()

def test_create_post(client):
    response = client.post("/create")
    assert response.data == b'Create'
    assert response.status_code == 200

def test_create_post_method_not_allowed(client):
    response = client.get("/create")
    assert response.status_code == 405
    assert sorted(response.allow) == ["POST"]

def test_create_post_with_invalid_data(client):
    response = client.post("/create", data={})
    assert response.data == b'Create'  # Assuming the method does not validate input
    assert response.status_code == 200

def test_create_post_with_unexpected_method(client):
    response = client.put("/create")
    assert response.status_code == 405
    assert sorted(response.allow) == ["POST"]
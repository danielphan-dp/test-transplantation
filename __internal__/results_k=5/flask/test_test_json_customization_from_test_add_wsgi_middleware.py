import pytest
from flask import Flask, json

@pytest.fixture
def app():
    app = Flask(__name__)

    @app.route("/create", methods=["POST"])
    def create():
        return 'Create'

    return app

def test_create_endpoint(client):
    response = client.post("/create")
    assert response.data == b'Create'
    assert response.status_code == 200

def test_create_with_invalid_method(client):
    response = client.get("/create")
    assert response.status_code == 405  # Method Not Allowed

def test_create_with_data(client):
    response = client.post("/create", data=json.dumps({"key": "value"}), content_type='application/json')
    assert response.data == b'Create'
    assert response.status_code == 200

def test_create_empty_request(client):
    response = client.post("/create", data=json.dumps({}), content_type='application/json')
    assert response.data == b'Create'
    assert response.status_code == 200
import pytest
from flask import Flask, json

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

def test_create_endpoint(client):
    response = client.post("/create")
    assert response.data.decode() == 'Create'
    assert response.status_code == 200

def test_create_with_invalid_data(client):
    response = client.post("/create", data=json.dumps({"invalid": "data"}), content_type='application/json')
    assert response.data.decode() == 'Create'
    assert response.status_code == 200

def test_create_with_no_data(client):
    response = client.post("/create", data=json.dumps({}), content_type='application/json')
    assert response.data.decode() == 'Create'
    assert response.status_code == 200
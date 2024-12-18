import pytest
import flask
import json

@pytest.fixture
def app():
    app = flask.Flask(__name__)

    @app.route("/create", methods=["POST"])
    def create():
        return 'Create'

    return app

def test_create(client):
    response = client.post("/create")
    assert response.data == b'Create'
    assert response.status_code == 200

def test_create_with_json(client):
    response = client.post(
        "/create",
        data=json.dumps({"key": "value"}),
        content_type="application/json"
    )
    assert response.data == b'Create'
    assert response.status_code == 200

def test_create_empty_json(client):
    response = client.post(
        "/create",
        data=json.dumps({}),
        content_type="application/json"
    )
    assert response.data == b'Create'
    assert response.status_code == 200

def test_create_invalid_method(client):
    response = client.get("/create")
    assert response.status_code == 405  # Method Not Allowed
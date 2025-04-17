import pytest
from flask import Flask, request
from flask.testing import FlaskClient

@pytest.fixture
def app():
    app = Flask(__name__)

    @app.post("/")
    def create():
        return 'Create'

    return app

def test_create_endpoint(client: FlaskClient) -> None:
    rv = client.post("/")
    assert rv.data == b'Create'
    assert rv.status_code == 200

def test_create_with_invalid_data(client: FlaskClient) -> None:
    rv = client.post("/", data={"invalid": "data"})
    assert rv.data == b'Create'
    assert rv.status_code == 200

def test_create_with_empty_request(client: FlaskClient) -> None:
    rv = client.post("/")
    assert rv.data == b'Create'
    assert rv.status_code == 200

def test_create_with_large_payload(client: FlaskClient) -> None:
    rv = client.post("/", data={"myfile": "x" * 1000})
    assert rv.data == b'Create'
    assert rv.status_code == 200

def test_create_with_json(client: FlaskClient) -> None:
    rv = client.post("/", json={"key": "value"})
    assert rv.data == b'Create'
    assert rv.status_code == 200
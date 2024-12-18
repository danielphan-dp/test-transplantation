import pytest
from flask import Flask
from flask.testing import FlaskClient

@pytest.fixture
def app() -> Flask:
    app = Flask(__name__)
    return app

@pytest.fixture
def client(app: Flask) -> FlaskClient:
    return app.test_client()

def test_post_create(client: FlaskClient) -> None:
    response = client.post("/")
    assert response.data == b'Create'

def test_post_with_data(client: FlaskClient) -> None:
    response = client.post("/", data={"key": "value"})
    assert response.data == b'Create'

def test_post_empty_data(client: FlaskClient) -> None:
    response = client.post("/", data={})
    assert response.data == b'Create'

def test_post_invalid_method(client: FlaskClient) -> None:
    response = client.get("/")
    assert response.status_code == 405  # Method Not Allowed

def test_post_large_data(client: FlaskClient) -> None:
    app.config["MAX_CONTENT_LENGTH"] = 50
    response = client.post("/", data={"myfile": "foo" * 50})
    assert response.data == b"42"  # Assuming the error handler returns this for large data

def test_post_no_data(client: FlaskClient) -> None:
    response = client.post("/")
    assert response.data == b'Create'  # Ensure it still returns 'Create' with no data
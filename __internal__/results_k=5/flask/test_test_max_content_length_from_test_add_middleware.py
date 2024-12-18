import pytest
from flask import Flask, request
from flask.testing import FlaskClient

@pytest.fixture
def app() -> Flask:
    app = Flask(__name__)
    return app

@pytest.fixture
def client(app: Flask) -> FlaskClient:
    return app.test_client()

@app.post("/")
def create_post():
    return 'Create'

def test_create_post(client: FlaskClient) -> None:
    response = client.post("/")
    assert response.data == b'Create'

def test_create_post_with_data(client: FlaskClient) -> None:
    response = client.post("/", data={"title": "Test Title", "body": "Test Body"})
    assert response.data == b'Create'

def test_create_post_empty_data(client: FlaskClient) -> None:
    response = client.post("/", data={})
    assert response.data == b'Create'
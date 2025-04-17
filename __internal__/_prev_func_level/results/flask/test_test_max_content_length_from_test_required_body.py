import pytest
from flask import Flask, request
from flask.testing import FlaskClient

@pytest.fixture
def app():
    app = Flask(__name__)
    return app

@pytest.fixture
def client(app: Flask):
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
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

@app.post("/")
def create():
    return 'Create'

def test_create_post(client: FlaskClient) -> None:
    response = client.post("/")
    assert response.data == b'Create'

def test_create_post_with_data(client: FlaskClient) -> None:
    response = client.post("/", data={"key": "value"})
    assert response.data == b'Create'

def test_create_post_empty_data(client: FlaskClient) -> None:
    response = client.post("/", data={})
    assert response.data == b'Create'

def test_create_post_invalid_method(client: FlaskClient) -> None:
    response = client.get("/")
    assert response.status_code == 405  # Method Not Allowed

def test_create_post_large_data(client: FlaskClient) -> None:
    response = client.post("/", data={"myfile": "foo" * 100})
    assert response.data == b'Create'  # Assuming the method can handle large data without error
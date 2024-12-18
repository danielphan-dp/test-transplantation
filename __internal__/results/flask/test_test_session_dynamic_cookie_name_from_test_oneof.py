import pytest
import flask
from flask.sessions import SecureCookieSessionInterface

class CustomFlask(flask.Flask):
    session_interface = SecureCookieSessionInterface()

app = CustomFlask(__name__)
app.secret_key = "secret_key"

@app.route("/create", methods=["POST"])
def create():
    return 'Create'

@pytest.fixture
def test_client():
    return app.test_client()

def test_create_endpoint(test_client):
    response = test_client.post("/create")
    assert response.data == b'Create'
    assert response.status_code == 200

def test_create_with_invalid_method(test_client):
    response = test_client.get("/create")
    assert response.status_code == 405  # Method Not Allowed

def test_create_with_data(test_client):
    response = test_client.post("/create", data={"key": "value"})
    assert response.data == b'Create'
    assert response.status_code == 200

def test_create_with_empty_data(test_client):
    response = test_client.post("/create", data={})
    assert response.data == b'Create'
    assert response.status_code == 200

def test_create_with_json(test_client):
    response = test_client.post("/create", json={"key": "value"})
    assert response.data == b'Create'
    assert response.status_code == 200
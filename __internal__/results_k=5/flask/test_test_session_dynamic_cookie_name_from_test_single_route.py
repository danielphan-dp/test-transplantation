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

test_client = app.test_client()

def test_create_route():
    response = test_client.post("/create")
    assert response.data == b'Create'

def test_create_route_invalid_method():
    response = test_client.get("/create")
    assert response.status_code == 405

def test_create_route_with_data():
    response = test_client.post("/create", data={"key": "value"})
    assert response.data == b'Create'  # Ensure it still returns 'Create' regardless of data

def test_create_route_empty_post():
    response = test_client.post("/create", data={})
    assert response.data == b'Create'  # Ensure it still returns 'Create' with empty data

def test_create_route_with_additional_headers():
    response = test_client.post("/create", headers={"X-Custom-Header": "value"})
    assert response.data == b'Create'  # Ensure it still returns 'Create' with custom headers
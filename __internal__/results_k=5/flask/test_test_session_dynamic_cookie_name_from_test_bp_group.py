import pytest
import flask
from flask.sessions import SecureCookieSessionInterface

class CustomFlask(flask.Flask):
    session_interface = SecureCookieSessionInterface()

app = CustomFlask(__name__)
app.secret_key = "secret_key"

@app.route("/set", methods=["POST"])
def set():
    flask.session["value"] = flask.request.form["value"]
    return "value set"

@app.route("/get")
def get():
    v = flask.session.get("value", "None")
    return v

@pytest.fixture
def test_client():
    return app.test_client()

def test_get_without_setting_value(test_client):
    response = test_client.get("/get")
    assert response.data == b'None'

def test_get_after_setting_value(test_client):
    test_client.post("/set", data={"value": "100"})
    response = test_client.get("/get")
    assert response.data == b'100'

def test_get_with_different_value(test_client):
    test_client.post("/set", data={"value": "200"})
    response = test_client.get("/get")
    assert response.data == b'200'

def test_get_with_no_value_set(test_client):
    response = test_client.get("/get")
    assert response.data == b'None'
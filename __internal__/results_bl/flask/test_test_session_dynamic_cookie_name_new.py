import warnings
import pytest
import flask
from flask.globals import request_ctx
from flask.sessions import SecureCookieSessionInterface
from flask.sessions import SessionInterface
from greenlet import greenlet
from flask.testing import EnvironBuilder

class PathAwareSessionInterface(SecureCookieSessionInterface):
    def get_cookie_name(self, app):
        if flask.request.url.endswith("dynamic_cookie"):
            return "dynamic_cookie_name"
        else:
            return super().get_cookie_name(app)

class CustomFlask(flask.Flask):
    session_interface = PathAwareSessionInterface()

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

@app.route("/set_dynamic_cookie", methods=["POST"])
def set_dynamic_cookie():
    flask.session["value"] = flask.request.form["value"]
    return "value set"

@app.route("/get_dynamic_cookie")
def get_dynamic_cookie():
    v = flask.session.get("value", "None")
    return v

test_client = app.test_client()

def test_get_without_setting_value():
    response = test_client.get("/get")
    assert response.data == b'None'

def test_get_dynamic_cookie_without_setting_value():
    response = test_client.get("/get_dynamic_cookie")
    assert response.data == b'None'

def test_get_after_setting_value():
    test_client.post("/set", data={"value": "100"})
    response = test_client.get("/get")
    assert response.data == b'100'

def test_get_dynamic_cookie_after_setting_value():
    test_client.post("/set_dynamic_cookie", data={"value": "200"})
    response = test_client.get("/get_dynamic_cookie")
    assert response.data == b'200'

def test_get_after_overwriting_value():
    test_client.post("/set", data={"value": "300"})
    test_client.post("/set", data={"value": "400"})
    response = test_client.get("/get")
    assert response.data == b'400'

def test_get_dynamic_cookie_after_overwriting_value():
    test_client.post("/set_dynamic_cookie", data={"value": "500"})
    test_client.post("/set_dynamic_cookie", data={"value": "600"})
    response = test_client.get("/get_dynamic_cookie")
    assert response.data == b'600'
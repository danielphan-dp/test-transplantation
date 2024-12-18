import flask
import pytest

def test_get_session_value(app, client):
    @app.route("/set_value")
    def set_value():
        flask.session["value"] = "test_value"
        return ""

    rv = client.get("/set_value")
    assert "set-cookie" in rv.headers

    rv = client.get("/get")
    assert rv.data == b"test_value"

def test_get_session_value_default(app, client):
    rv = client.get("/get")
    assert rv.data == b'None'

def test_get_session_value_empty(app, client):
    @app.route("/set_empty_value")
    def set_empty_value():
        flask.session["value"] = ""
        return ""

    rv = client.get("/set_empty_value")
    assert "set-cookie" in rv.headers

    rv = client.get("/get")
    assert rv.data == b''
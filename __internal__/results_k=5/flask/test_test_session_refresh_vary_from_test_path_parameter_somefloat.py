import flask
import pytest

def test_get_session_value(app, client):
    @app.route("/set")
    def set_value():
        flask.session["value"] = "test_value"
        return ""

    @app.route("/get")
    def get_value():
        return flask.session.get('value', 'None')

    # Test setting a session value
    client.get("/set")
    rv = client.get("/get")
    assert rv.data.decode() == "test_value"

def test_get_session_value_default(app, client):
    @app.route("/get")
    def get_value():
        return flask.session.get('value', 'None')

    # Test getting a session value when none is set
    rv = client.get("/get")
    assert rv.data.decode() == "None"

def test_get_session_value_empty(app, client):
    @app.route("/set_empty")
    def set_empty_value():
        flask.session["value"] = ""
        return ""

    @app.route("/get")
    def get_value():
        return flask.session.get('value', 'None')

    # Test setting an empty session value
    client.get("/set_empty")
    rv = client.get("/get")
    assert rv.data.decode() == ""
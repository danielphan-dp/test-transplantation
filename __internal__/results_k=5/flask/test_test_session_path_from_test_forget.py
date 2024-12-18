import flask
import pytest

def test_get_session_value(app, client):
    app.config.update(APPLICATION_ROOT="/foo")

    @app.route("/set")
    def set_value():
        flask.session["value"] = "test_value"
        return "Value set"

    @app.route("/get")
    def get_value():
        return flask.session.get('value', 'None')

    client.get("/set")
    rv = client.get("/get")
    assert rv.data == b"test_value"

def test_get_session_value_default(app, client):
    app.config.update(APPLICATION_ROOT="/foo")

    @app.route("/get")
    def get_value():
        return flask.session.get('value', 'None')

    rv = client.get("/get")
    assert rv.data == b"None"

def test_get_session_value_after_clear(app, client):
    app.config.update(APPLICATION_ROOT="/foo")

    @app.route("/set")
    def set_value():
        flask.session["value"] = "test_value"
        return "Value set"

    @app.route("/clear")
    def clear_value():
        flask.session.clear()
        return "Session cleared"

    @app.route("/get")
    def get_value():
        return flask.session.get('value', 'None')

    client.get("/set")
    client.get("/clear")
    rv = client.get("/get")
    assert rv.data == b"None"
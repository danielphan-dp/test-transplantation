import flask
import pytest

def test_get_session_value(app, client):
    @app.route("/set")
    def set_value():
        flask.session['value'] = 'test_value'
        return "Value set"

    @app.route("/get")
    def get_value():
        return flask.session.get('value', 'None')

    # Test setting a session value
    rv = client.get("/set")
    assert rv.data == b"Value set"

    # Test getting the session value
    rv = client.get("/get")
    assert rv.data == b'test_value'

def test_get_session_value_default(app, client):
    @app.route("/get")
    def get_value():
        return flask.session.get('value', 'None')

    # Test getting the default session value when not set
    rv = client.get("/get")
    assert rv.data == b'None'

def test_get_session_value_after_clear(app, client):
    @app.route("/set")
    def set_value():
        flask.session['value'] = 'test_value'
        return "Value set"

    @app.route("/clear")
    def clear_value():
        flask.session.clear()
        return "Session cleared"

    @app.route("/get")
    def get_value():
        return flask.session.get('value', 'None')

    # Set a session value
    rv = client.get("/set")
    assert rv.data == b"Value set"

    # Clear the session
    rv = client.get("/clear")
    assert rv.data == b"Session cleared"

    # Test getting the session value after clearing
    rv = client.get("/get")
    assert rv.data == b'None'
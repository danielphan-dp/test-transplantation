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

    # Set the session value
    client.get("/set")
    
    # Test getting the session value
    rv = client.get("/get")
    assert rv.data == b"test_value"

def test_get_session_value_default(app, client):
    @app.route("/get")
    def get_value():
        return flask.session.get('value', 'None')

    # Test getting the session value when it is not set
    rv = client.get("/get")
    assert rv.data == b"None"
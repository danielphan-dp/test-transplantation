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

    # Set the session value
    rv = client.get("/set", "http://www.example.com:8080/test/")
    assert rv.data == b"Value set"

    # Retrieve the session value
    rv = client.get("/get", "http://www.example.com:8080/test/")
    assert rv.data == b"test_value"

def test_get_session_value_default(app, client):
    @app.route("/get")
    def get_value():
        return flask.session.get('value', 'None')

    # Retrieve the session value without setting it
    rv = client.get("/get", "http://www.example.com:8080/test/")
    assert rv.data == b'None'

def test_get_session_value_after_clear(app, client):
    @app.route("/set")
    def set_value():
        flask.session['value'] = 'test_value'
        return "Value set"

    @app.route("/clear")
    def clear():
        flask.session.pop("value", None)
        return "Value cleared"

    # Set the session value
    rv = client.get("/set", "http://www.example.com:8080/test/")
    assert rv.data == b"Value set"

    # Clear the session value
    rv = client.get("/clear", "http://www.example.com:8080/test/")
    assert rv.data == b"Value cleared"

    # Retrieve the session value after clearing
    rv = client.get("/get", "http://www.example.com:8080/test/")
    assert rv.data == b'None'
import flask
import pytest

def test_get_value_from_session(app, client):
    @app.route("/set/<value>")
    def set_value(value):
        flask.session['value'] = value
        return "Value set"

    @app.route("/get")
    def get():
        v = flask.session.get('value', 'None')
        return v

    # Test setting a value in the session
    response = client.get("/set/test_value")
    assert response.data == b"Value set"

    # Test getting the value from the session
    response = client.get("/get")
    assert response.data == b"test_value"

def test_get_value_not_set(app, client):
    @app.route("/get")
    def get():
        v = flask.session.get('value', 'None')
        return v

    # Test getting the value when it is not set
    response = client.get("/get")
    assert response.data == b'None'
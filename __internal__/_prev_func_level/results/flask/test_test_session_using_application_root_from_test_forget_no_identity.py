import flask
import pytest

def test_get_session_value_none(app, client):
    @app.route("/set")
    def set_value():
        flask.session['value'] = None
        return "Value set to None"

    client.get("/set")
    response = client.get("/get")
    assert response.data == b'None'

def test_get_session_value_set(app, client):
    @app.route("/set")
    def set_value():
        flask.session['value'] = 'Test Value'
        return "Value set"

    client.get("/set")
    response = client.get("/get")
    assert response.data == b'Test Value'

def test_get_session_value_default(app, client):
    response = client.get("/get")
    assert response.data == b'None'

def test_get_session_value_empty_string(app, client):
    @app.route("/set")
    def set_value():
        flask.session['value'] = ''
        return "Value set to empty string"

    client.get("/set")
    response = client.get("/get")
    assert response.data == b''
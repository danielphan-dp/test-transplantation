import flask
import pytest

def test_session_get_value_none(app, client):
    @app.route("/set_none")
    def set_none():
        flask.session['value'] = None
        return "Set to None"

    client.get("/set_none")
    assert client.get('/get').data == b'None'

def test_session_get_value_string(app, client):
    @app.route("/set_string")
    def set_string():
        flask.session['value'] = "Hello"
        return "Set to Hello"

    client.get("/set_string")
    assert client.get('/get').data == b'Hello'

def test_session_get_value_integer(app, client):
    @app.route("/set_integer")
    def set_integer():
        flask.session['value'] = 123
        return "Set to 123"

    client.get("/set_integer")
    assert client.get('/get').data == b'123'

def test_session_get_value_empty_string(app, client):
    @app.route("/set_empty_string")
    def set_empty_string():
        flask.session['value'] = ""
        return "Set to empty string"

    client.get("/set_empty_string")
    assert client.get('/get').data == b''

def test_session_get_value_boolean(app, client):
    @app.route("/set_boolean")
    def set_boolean():
        flask.session['value'] = True
        return "Set to True"

    client.get("/set_boolean")
    assert client.get('/get').data == b'True'
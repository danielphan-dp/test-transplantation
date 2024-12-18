import flask
import pytest

def test_session_get_value_none(app, client):
    @app.route("/set_none")
    def set_none():
        flask.session['value'] = None
        return "Set to None"

    client.get("/set_none")
    assert client.get('/get').data == b'None'

def test_session_get_value_set(app, client):
    @app.route("/set_value")
    def set_value():
        flask.session['value'] = 'Test Value'
        return "Set to Test Value"

    client.get("/set_value")
    assert client.get('/get').data == b'Test Value'

def test_session_get_value_empty_string(app, client):
    @app.route("/set_empty")
    def set_empty():
        flask.session['value'] = ''
        return "Set to Empty String"

    client.get("/set_empty")
    assert client.get('/get').data == b''

def test_session_get_value_integer(app, client):
    @app.route("/set_integer")
    def set_integer():
        flask.session['value'] = 123
        return "Set to Integer"

    client.get("/set_integer")
    assert client.get('/get').data == b'123'

def test_session_get_value_boolean(app, client):
    @app.route("/set_boolean")
    def set_boolean():
        flask.session['value'] = True
        return "Set to Boolean"

    client.get("/set_boolean")
    assert client.get('/get').data == b'True'
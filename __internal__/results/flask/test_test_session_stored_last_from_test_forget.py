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
        flask.session['value'] = 'test_value'
        return "Set to test_value"

    client.get("/set_value")
    assert client.get('/get').data == b'test_value'

def test_session_get_value_empty_string(app, client):
    @app.route("/set_empty")
    def set_empty():
        flask.session['value'] = ''
        return "Set to empty string"

    client.get("/set_empty")
    assert client.get('/get').data == b''

def test_session_get_value_nonexistent(app, client):
    assert client.get('/get').data == b'None'
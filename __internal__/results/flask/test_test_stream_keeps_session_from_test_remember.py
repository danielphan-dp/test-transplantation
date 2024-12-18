import flask
import pytest

def test_get_session_value_none(self, app, client):
    @app.route("/set")
    def set_value():
        flask.session['value'] = None
        return "Value set"

    client.get("/set")
    rv = client.get("/get")
    assert rv.data == b'None'

def test_get_session_value_set(self, app, client):
    @app.route("/set")
    def set_value():
        flask.session['value'] = 'test_value'
        return "Value set"

    client.get("/set")
    rv = client.get("/get")
    assert rv.data == b'test_value'

def test_get_session_value_empty_string(self, app, client):
    @app.route("/set")
    def set_value():
        flask.session['value'] = ''
        return "Value set"

    client.get("/set")
    rv = client.get("/get")
    assert rv.data == b''

def test_get_session_value_nonexistent(self, app, client):
    rv = client.get("/get")
    assert rv.data == b'None'
import flask
import pytest

def test_get_session_value_none(app, client):
    @app.route("/get")
    def get():
        v = flask.session.get('value', 'None')
        return v

    rv = client.get("/get")
    assert rv.data == b'None'

def test_get_session_value_set(app, client):
    @app.route("/set")
    def set_value():
        flask.session['value'] = 'test_value'
        return ""

    client.get("/set")
    rv = client.get("/get")
    assert rv.data == b'test_value'

def test_get_session_value_empty(app, client):
    @app.route("/set_empty")
    def set_empty_value():
        flask.session['value'] = ''
        return ""

    client.get("/set_empty")
    rv = client.get("/get")
    assert rv.data == b''
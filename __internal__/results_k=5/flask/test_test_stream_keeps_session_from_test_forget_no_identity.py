import flask
import pytest

def test_get_session_value_none(self, app, client):
    @app.route("/set")
    def set_value():
        flask.session['value'] = None
        return "Value set"

    @app.route("/get")
    def get_value():
        return flask.session.get('value', 'None')

    client.get("/set")
    rv = client.get("/get")
    assert rv.data == b'None'

def test_get_session_value_set(self, app, client):
    @app.route("/set")
    def set_value():
        flask.session['value'] = 'test_value'
        return "Value set"

    @app.route("/get")
    def get_value():
        return flask.session.get('value', 'None')

    client.get("/set")
    rv = client.get("/get")
    assert rv.data == b'test_value'

def test_get_session_value_default(self, app, client):
    @app.route("/get")
    def get_value():
        return flask.session.get('value', 'default_value')

    rv = client.get("/get")
    assert rv.data == b'default_value'
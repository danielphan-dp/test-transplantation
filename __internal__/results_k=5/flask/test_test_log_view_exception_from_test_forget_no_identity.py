import flask
import pytest
from io import StringIO

def test_get_value_from_session(app, client):
    @app.route("/set")
    def set_value():
        flask.session['value'] = 'test_value'
        return "Value set"

    @app.route("/get")
    def get_value():
        return flask.session.get('value', 'None')

    app.testing = True
    client.get("/set")
    rv = client.get("/get")
    assert rv.data == b'test_value'

def test_get_value_not_set(app, client):
    @app.route("/get")
    def get_value():
        return flask.session.get('value', 'None')

    app.testing = True
    rv = client.get("/get")
    assert rv.data == b'None'

def test_get_value_with_none_default(app, client):
    @app.route("/set_none")
    def set_none():
        flask.session['value'] = None
        return "None set"

    @app.route("/get")
    def get_value():
        return flask.session.get('value', 'None')

    app.testing = True
    client.get("/set_none")
    rv = client.get("/get")
    assert rv.data == b'None'
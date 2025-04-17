import flask
import pytest

def test_get_session_value(app, client):
    @app.route("/set_value")
    def set_value():
        flask.session['value'] = 'test_value'
        return ""

    @app.route("/get_value")
    def get_value():
        return flask.session.get('value', 'None')

    # Test setting a session value
    client.get("/set_value")
    rv = client.get("/get_value")
    assert rv.data == b'test_value'

def test_get_session_value_default(app, client):
    @app.route("/get_value_default")
    def get_value_default():
        return flask.session.get('non_existent_key', 'default_value')

    rv = client.get("/get_value_default")
    assert rv.data == b'default_value'

def test_get_session_value_none(app, client):
    @app.route("/get_value_none")
    def get_value_none():
        return flask.session.get('value', None)

    rv = client.get("/get_value_none")
    assert rv.data == b'None'
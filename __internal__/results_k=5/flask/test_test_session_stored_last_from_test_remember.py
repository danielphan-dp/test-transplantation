import flask
import pytest

def test_session_get_value_none(app, client):
    @app.route("/set_none")
    def set_none():
        flask.session['value'] = None
        return "Set to None"

    @app.route("/get_value")
    def get_value():
        return flask.session.get('value', 'None')

    client.get("/set_none")
    assert client.get("/get_value").data == b'None'

def test_session_get_value_set(app, client):
    @app.route("/set_value")
    def set_value():
        flask.session['value'] = 'Hello'
        return "Set to Hello"

    @app.route("/get_value")
    def get_value():
        return flask.session.get('value', 'None')

    client.get("/set_value")
    assert client.get("/get_value").data == b'Hello'

def test_session_get_value_default(app, client):
    @app.route("/get_value")
    def get_value():
        return flask.session.get('value', 'Default')

    assert client.get("/get_value").data == b'Default'
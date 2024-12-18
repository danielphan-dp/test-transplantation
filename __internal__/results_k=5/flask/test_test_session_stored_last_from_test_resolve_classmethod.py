import flask
import pytest

def test_session_get_value_none(app, client):
    @app.route("/set_none")
    def set_none():
        flask.session["value"] = None
        return ""

    @app.route("/get")
    def get():
        v = flask.session.get('value', 'None')
        return v

    client.get("/set_none")
    assert client.get("/get").data == b'None'

def test_session_get_value_set(app, client):
    @app.route("/set_value")
    def set_value():
        flask.session["value"] = "TestValue"
        return ""

    @app.route("/get")
    def get():
        v = flask.session.get('value', 'None')
        return v

    client.get("/set_value")
    assert client.get("/get").data == b'TestValue'

def test_session_get_value_default(app, client):
    @app.route("/get")
    def get():
        v = flask.session.get('non_existent_key', 'DefaultValue')
        return v

    assert client.get("/get").data == b'DefaultValue'
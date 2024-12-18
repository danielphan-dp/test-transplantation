import flask
import pytest

def test_get_method_with_session_value(app, client):
    @app.route("/set")
    def set_value():
        flask.session['value'] = 'test_value'
        return "Value set!"

    @app.route("/get")
    def get_value():
        return flask.session.get('value', 'None')

    client.get("/set")
    rv = client.get("/get")
    assert rv.data == b'test_value'

def test_get_method_without_session_value(app, client):
    @app.route("/get")
    def get_value():
        return flask.session.get('value', 'None')

    rv = client.get("/get")
    assert rv.data == b'None'
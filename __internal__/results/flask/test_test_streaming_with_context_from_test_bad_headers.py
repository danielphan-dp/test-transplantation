import flask
import pytest

def test_get_value_from_session(app, client):
    @app.route("/set")
    def set_value():
        flask.session['value'] = 'Test Value'
        return "Value Set"

    @app.route("/get")
    def get_value():
        return flask.session.get('value', 'None')

    client.get("/set")
    rv = client.get("/get")
    assert rv.data == b'Test Value'

def test_get_value_not_set(app, client):
    @app.route("/get")
    def get_value():
        return flask.session.get('value', 'None')

    rv = client.get("/get")
    assert rv.data == b'None'
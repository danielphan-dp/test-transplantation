import flask
import pytest

def test_get_session_value(app, client):
    @app.route("/set")
    def set_session_value():
        flask.session['value'] = 'test_value'
        return "", 204

    @app.route("/get")
    def get_session_value():
        return flask.session.get('value', 'None')

    with client:
        client.get("/set")
        response = client.get("/get")
        assert response.data == b'test_value'

def test_get_session_value_default(app, client):
    @app.route("/get")
    def get_session_value():
        return flask.session.get('value', 'None')

    with client:
        response = client.get("/get")
        assert response.data == b'None'

def test_get_session_value_none(app, client):
    @app.route("/set_none")
    def set_none_session_value():
        flask.session['value'] = None
        return "", 204

    @app.route("/get")
    def get_session_value():
        return flask.session.get('value', 'None')

    with client:
        client.get("/set_none")
        response = client.get("/get")
        assert response.data == b'None'
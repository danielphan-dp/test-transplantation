import flask
import pytest

def test_get_session_value(app, client):
    app.testing = True

    @app.route("/set")
    def set_value():
        flask.session['value'] = 'test_value'
        return "Value set"

    @app.route("/get")
    def get_value():
        return flask.session.get('value', 'None')

    client.get("/set")
    response = client.get("/get")
    assert response.data == b'test_value'

def test_get_session_value_default(app, client):
    app.testing = True

    response = client.get("/get")
    assert response.data == b'None'

def test_get_session_value_empty(app, client):
    app.testing = True

    @app.route("/set_empty")
    def set_empty_value():
        flask.session['value'] = ''
        return "Empty value set"

    client.get("/set_empty")
    response = client.get("/get")
    assert response.data == b''
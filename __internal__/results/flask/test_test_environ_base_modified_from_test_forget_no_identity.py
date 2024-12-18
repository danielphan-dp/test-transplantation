import flask
import pytest

def test_get_value_from_session(app, client):
    @app.route("/set")
    def set_value():
        flask.session['value'] = 'test_value'
        return ""

    @app.route("/get")
    def get_value():
        return flask.session.get('value', 'None')

    client.get("/set")
    response = client.get("/get")
    assert response.data.decode() == 'test_value'

def test_get_value_not_set(app, client):
    @app.route("/get")
    def get_value():
        return flask.session.get('value', 'None')

    response = client.get("/get")
    assert response.data.decode() == 'None'
import flask
import pytest

def test_get_value_from_session(app, client):
    app.config["SERVER_NAME"] = "example.com"
    
    @app.route("/set/<value>")
    def set_value(value):
        flask.session['value'] = value
        return "Value set"

    @app.route("/get")
    def get():
        v = flask.session.get('value', 'None')
        return v

    with client:
        response_set = client.get('/set/test_value')
        assert response_set.status_code == 200
        assert b"Value set" in response_set.data

        response_get = client.get('/get')
        assert response_get.status_code == 200
        assert response_get.data == b'test_value'

def test_get_value_not_set(app, client):
    @app.route("/get")
    def get():
        v = flask.session.get('value', 'None')
        return v

    with client:
        response = client.get('/get')
        assert response.status_code == 200
        assert response.data == b'None'
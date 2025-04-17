import flask
import pytest

def test_get_value_from_session(app, client):
    app.secret_key = 'test_secret'
    
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

def test_get_value_not_set(app, client):
    app.secret_key = 'test_secret'
    
    @app.route("/get")
    def get_value():
        return flask.session.get('value', 'None')

    response = client.get("/get")
    assert response.data == b'None'
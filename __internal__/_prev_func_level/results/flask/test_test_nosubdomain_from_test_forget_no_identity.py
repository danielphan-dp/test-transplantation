import flask
import pytest

def test_get_value_from_session(app, client):
    app.config["SERVER_NAME"] = "example.com"
    
    @app.route("/set")
    def set_value():
        flask.session['value'] = 'test_value'
        return "Value set"

    @app.route("/get")
    def get_value():
        return flask.session.get('value', 'None')

    with client:
        client.get("/set")
        response = client.get("/get")
        
    assert response.status_code == 200
    assert response.data == b'test_value'

def test_get_value_not_set(app, client):
    app.config["SERVER_NAME"] = "example.com"

    @app.route("/get")
    def get_value():
        return flask.session.get('value', 'None')

    with client:
        response = client.get("/get")
        
    assert response.status_code == 200
    assert response.data == b'None'
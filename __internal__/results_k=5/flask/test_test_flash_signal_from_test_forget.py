import flask
import pytest

def test_get_value_from_session(app):
    @app.route("/set")
    def set_value():
        flask.session['value'] = 'test_value'
        return "Value set"

    @app.route("/get")
    def get_value():
        return flask.session.get('value', 'None')

    client = app.test_client()
    
    with client.session_transaction() as session:
        session['value'] = 'test_value'
    
    response = client.get("/get")
    assert response.data.decode() == 'test_value'

def test_get_value_not_set(app):
    @app.route("/get")
    def get_value():
        return flask.session.get('value', 'None')

    client = app.test_client()
    
    response = client.get("/get")
    assert response.data.decode() == 'None'
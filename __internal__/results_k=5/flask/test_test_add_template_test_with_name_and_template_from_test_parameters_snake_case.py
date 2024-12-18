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

    # Set a value in the session
    client.get("/set")
    
    # Test getting the value from the session
    rv = client.get("/get")
    assert rv.data == b'Test Value'

def test_get_value_from_session_default(app, client):
    @app.route("/get")
    def get_value():
        return flask.session.get('value', 'None')

    # Test getting the default value when session is empty
    rv = client.get("/get")
    assert rv.data == b'None'

def test_get_value_from_session_after_clear(app, client):
    @app.route("/set")
    def set_value():
        flask.session['value'] = 'Test Value'
        return "Value Set"

    @app.route("/clear")
    def clear_session():
        flask.session.clear()
        return "Session Cleared"

    @app.route("/get")
    def get_value():
        return flask.session.get('value', 'None')

    # Set a value in the session
    client.get("/set")
    # Clear the session
    client.get("/clear")
    
    # Test getting the value after clearing the session
    rv = client.get("/get")
    assert rv.data == b'None'
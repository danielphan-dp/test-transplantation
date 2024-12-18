import flask
import pytest

def test_get_session_value(app, client):
    """Test retrieval of session value."""
    
    @app.route("/set_value")
    def set_value():
        flask.session['value'] = 'test_value'
        return "Value set"

    @app.route("/get")
    def get():
        v = flask.session.get('value', 'None')
        return v

    # Test default session value
    rv = client.get("/get")
    assert rv.data == b'None'
    
    # Set session value and test retrieval
    client.get("/set_value")
    rv = client.get("/get")
    assert rv.data == b'test_value'

def test_get_session_value_empty(app, client):
    """Test retrieval of session value when session is empty."""
    
    @app.route("/get")
    def get():
        v = flask.session.get('value', 'None')
        return v

    rv = client.get("/get")
    assert rv.data == b'None'

def test_get_session_value_none(app, client):
    """Test retrieval of session value when session key does not exist."""
    
    @app.route("/get")
    def get():
        v = flask.session.get('non_existent_key', 'None')
        return v

    rv = client.get("/get")
    assert rv.data == b'None'
import flask
import pytest
from werkzeug.exceptions import BadRequest

def test_get_value_from_session(app, client):
    @app.route("/set")
    def set_value():
        flask.session['value'] = 'test_value'
        return 'Value set'

    @app.route("/clear")
    def clear_value():
        flask.session.pop('value', None)
        return 'Value cleared'

    # Test when session has a value
    client.get("/set")
    rv = client.get("/get")
    assert rv.data == b'test_value'

    # Test when session is empty
    client.get("/clear")
    rv = client.get("/get")
    assert rv.data == b'None'

def test_get_value_with_no_session(app, client):
    rv = client.get("/get")
    assert rv.data == b'None'

def test_get_value_with_different_session_value(app, client):
    @app.route("/set_different")
    def set_different_value():
        flask.session['value'] = 'another_value'
        return 'Different value set'

    client.get("/set_different")
    rv = client.get("/get")
    assert rv.data == b'another_value'
import flask
import pytest

def test_get_value_from_session(app, client):
    app.testing = True

    @app.route("/set/<value>")
    def set_value(value):
        flask.session['value'] = value
        return "Value set"

    @app.route("/get")
    def get():
        v = flask.session.get('value', 'None')
        return v

    # Test default session value
    rv = client.get("/get")
    assert rv.data == b'None'

    # Test setting a value in the session
    rv = client.get("/set/test_value")
    assert rv.data == b'Value set'

    # Test retrieving the set value from the session
    rv = client.get("/get")
    assert rv.data == b'test_value'

    # Test clearing the session
    with client.session_transaction() as session:
        session.clear()

    rv = client.get("/get")
    assert rv.data == b'None'
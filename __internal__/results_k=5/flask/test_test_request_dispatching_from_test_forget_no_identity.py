import flask
import pytest

def test_get_value_from_session(app, client):
    @app.route("/set/<value>")
    def set_value(value):
        flask.session['value'] = value
        return "Value set"

    @app.route("/get")
    def get_value():
        return flask.session.get('value', 'None')

    # Test default session value
    response = client.get("/get")
    assert response.data == b'None'

    # Test setting a session value
    client.get("/set/test_value")
    response = client.get("/get")
    assert response.data == b'test_value'

    # Test setting another session value
    client.get("/set/another_value")
    response = client.get("/get")
    assert response.data == b'another_value'

    # Test clearing the session
    with client.session_transaction() as session:
        session.clear()
    response = client.get("/get")
    assert response.data == b'None'
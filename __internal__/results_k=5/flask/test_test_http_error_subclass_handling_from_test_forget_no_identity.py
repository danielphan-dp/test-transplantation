import flask
import pytest

def test_get_session_value(app, client):
    @app.route("/set/<value>")
    def set_value(value):
        flask.session['value'] = value
        return "Value set"

    @app.route("/get")
    def get_value():
        return flask.session.get('value', 'None')

    # Test setting a value in the session
    client.get("/set/test_value")
    response = client.get("/get")
    assert response.data == b'test_value'

    # Test getting a value when none is set
    with client.session_transaction() as session:
        session.clear()
    response = client.get("/get")
    assert response.data == b'None'

    # Test setting a different value
    client.get("/set/another_value")
    response = client.get("/get")
    assert response.data == b'another_value'
import flask
import pytest

def test_get_session_value(app, client):
    @app.route("/set")
    def set_value():
        flask.session["value"] = "test_value"
        return "Value set"

    @app.route("/get")
    def get_value():
        return flask.session.get('value', 'None')

    # Test default session value when not set
    response = client.get("/get")
    assert response.data == b'None'

    # Set session value and test retrieval
    client.get("/set")
    response = client.get("/get")
    assert response.data == b'test_value'

    # Test session value after clearing session
    with client.session_transaction() as session:
        session.clear()
    response = client.get("/get")
    assert response.data == b'None'

    # Test session with different value
    @app.route("/set_another")
    def set_another_value():
        flask.session["value"] = "another_value"
        return "Another value set"

    client.get("/set_another")
    response = client.get("/get")
    assert response.data == b'another_value'
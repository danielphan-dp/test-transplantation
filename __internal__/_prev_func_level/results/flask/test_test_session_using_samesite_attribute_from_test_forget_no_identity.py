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
    rv = client.get("/get")
    assert rv.data == b'None'

    # Set session value and test retrieval
    client.get("/set")
    rv = client.get("/get")
    assert rv.data == b'test_value'

    # Test session value after clearing session
    with client.session_transaction() as session:
        session.clear()
    rv = client.get("/get")
    assert rv.data == b'None'

    # Test session with a different value
    @app.route("/set_another")
    def set_another_value():
        flask.session["value"] = "another_value"
        return "Another value set"

    client.get("/set_another")
    rv = client.get("/get")
    assert rv.data == b'another_value'
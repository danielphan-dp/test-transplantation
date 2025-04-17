import flask
import pytest

def test_get_session_value(app, client):
    @app.route("/set_value")
    def set_value():
        flask.session["value"] = "test_value"
        return ""

    @app.route("/clear_session")
    def clear_session():
        flask.session.clear()
        return ""

    # Test setting a session value
    client.get("/set_value")
    rv = client.get("/get")
    assert rv.data.decode() == "test_value"

    # Test getting a session value when it is not set
    client.get("/clear_session")
    rv = client.get("/get")
    assert rv.data.decode() == "None"

    # Test getting a session value after clearing
    client.get("/set_value")
    client.get("/clear_session")
    rv = client.get("/get")
    assert rv.data.decode() == "None"
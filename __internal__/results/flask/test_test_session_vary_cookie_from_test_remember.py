import flask
import pytest

def test_get_session_value(app, client):
    @app.route("/set_value")
    def set_value():
        flask.session["value"] = "test_value"
        return ""

    @app.route("/get")
    def get():
        return flask.session.get("value", "None")

    # Test setting a session value
    client.get("/set_value")
    rv = client.get("/get")
    assert rv.data.decode() == "test_value"

    # Test getting a session value when it is not set
    flask.session.clear()
    rv = client.get("/get")
    assert rv.data.decode() == "None"

    # Test getting a session value after clearing the session
    client.get("/set_value")
    flask.session.clear()
    rv = client.get("/get")
    assert rv.data.decode() == "None"
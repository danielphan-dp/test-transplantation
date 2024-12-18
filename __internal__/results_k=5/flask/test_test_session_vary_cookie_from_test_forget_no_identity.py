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

    # Test when session value is set
    client.get("/set_value")
    rv = client.get("/get")
    assert rv.data == b"test_value"

    # Test when session value is not set
    flask.session.clear()
    rv = client.get("/get")
    assert rv.data == b"None"

    # Test when session is cleared
    client.get("/set_value")
    flask.session.clear()
    rv = client.get("/get")
    assert rv.data == b"None"
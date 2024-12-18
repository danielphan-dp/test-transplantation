import flask
import pytest

def test_get_session_value(app, client, app_ctx):
    @app.route("/setvalue")
    def set_value():
        flask.session["value"] = "test_value"
        return "value set"

    @app.route("/get")
    def get():
        v = flask.session.get('value', 'None')
        return v

    with client:
        rv = client.get("/setvalue")
        assert rv.data == b"value set"
        assert flask.session.get("value") == "test_value"

        rv = client.get("/get")
        assert rv.data == b"test_value"

        flask.session.pop("value", None)  # Clear the session value
        rv = client.get("/get")
        assert rv.data == b'None'
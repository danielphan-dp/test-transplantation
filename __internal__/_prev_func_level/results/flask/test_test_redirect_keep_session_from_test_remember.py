import flask
import pytest

def test_get_value_from_session(app, client, app_ctx):
    @app.route("/setvalue", methods=["POST"])
    def set_value():
        flask.session["value"] = "test_value"
        return "Value set"

    @app.route("/get")
    def get():
        v = flask.session.get('value', 'None')
        return v

    with client:
        # Test default value when session is empty
        rv = client.get("/get")
        assert rv.data == b'None'

        # Set a value in the session
        rv = client.post("/setvalue")
        assert rv.data == b'Value set'
        assert flask.session.get("value") == "test_value"

        # Test getting the value from session
        rv = client.get("/get")
        assert rv.data == b'test_value'

        # Clear the session and test default value again
        flask.session.clear()
        rv = client.get("/get")
        assert rv.data == b'None'
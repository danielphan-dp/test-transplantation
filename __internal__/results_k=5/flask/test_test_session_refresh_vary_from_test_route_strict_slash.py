import flask
import pytest

def test_get_session_value(app, client):
    @app.route("/set_value")
    def set_value():
        flask.session["value"] = "test_value"
        return ""

    @app.route("/get")
    def get():
        v = flask.session.get('value', 'None')
        return v

    # Set a session value
    client.get("/set_value")
    rv = client.get("/get")
    assert rv.data.decode() == "test_value"

def test_get_session_value_default(app, client):
    @app.route("/get")
    def get():
        v = flask.session.get('value', 'None')
        return v

    rv = client.get("/get")
    assert rv.data.decode() == "None"
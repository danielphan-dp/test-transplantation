import flask
import pytest

def test_get_session_value(app, client):
    @app.route("/set_value", methods=["POST"])
    def set_value():
        flask.session["value"] = "test_value"
        return ""

    @app.route("/get")
    def get_value():
        return flask.session.get('value', 'None')

    client.post("/set_value")
    response = client.get("/get")
    assert response.data.decode() == "test_value"

def test_get_session_value_default(app, client):
    @app.route("/get")
    def get_value():
        return flask.session.get('value', 'None')

    response = client.get("/get")
    assert response.data.decode() == "None"

def test_get_session_value_after_clear(app, client):
    @app.route("/set_value", methods=["POST"])
    def set_value():
        flask.session["value"] = "test_value"
        return ""

    @app.route("/clear_session", methods=["POST"])
    def clear_session():
        flask.session.clear()
        return ""

    client.post("/set_value")
    client.post("/clear_session")
    response = client.get("/get")
    assert response.data.decode() == "None"
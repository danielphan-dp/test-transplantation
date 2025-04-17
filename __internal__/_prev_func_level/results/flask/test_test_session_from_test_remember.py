import flask
import pytest

def test_get_session_value(app, client):
    @app.route("/set", methods=["POST"])
    def set_value():
        flask.session["value"] = flask.request.form["value"]
        return "value set"

    @app.route("/get")
    def get_value():
        v = flask.session.get("value", "None")
        return v

    # Test getting value when session is empty
    assert client.get("/get").data == b"None"

    # Test setting and getting a value
    assert client.post("/set", data={"value": "100"}).data == b"value set"
    assert client.get("/get").data == b"100"

    # Test getting value after clearing session
    with client.session_transaction() as session:
        session.clear()
    assert client.get("/get").data == b"None"

def test_get_session_value_with_different_data(app, client):
    @app.route("/set", methods=["POST"])
    def set_value():
        flask.session["value"] = flask.request.form["value"]
        return "value set"

    assert client.post("/set", data={"value": "Hello"}).data == b"value set"
    assert client.get("/get").data == b"Hello"

    assert client.post("/set", data={"value": "World"}).data == b"value set"
    assert client.get("/get").data == b"World"
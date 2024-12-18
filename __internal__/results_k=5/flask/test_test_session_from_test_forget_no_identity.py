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

    # Test when session is empty
    assert client.get("/get").data == b"None"

    # Test setting a value in the session
    assert client.post("/set", data={"value": "100"}).data == b"value set"
    assert client.get("/get").data == b"100"

    # Test setting another value in the session
    assert client.post("/set", data={"value": "200"}).data == b"value set"
    assert client.get("/get").data == b"200"

    # Test clearing the session
    with client.session_transaction() as session:
        session.clear()
    assert client.get("/get").data == b"None"
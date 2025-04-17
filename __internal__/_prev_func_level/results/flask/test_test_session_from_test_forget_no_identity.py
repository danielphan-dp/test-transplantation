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

    # Test overwriting the session value
    assert client.post("/set", data={"value": "200"}).data == b"value set"
    assert client.get("/get").data == b"200"

    # Test session access and modification flags
    with app.test_request_context():
        assert not flask.session.accessed
        assert not flask.session.modified
        flask.session["value"] = "300"
        assert flask.session.accessed
        assert flask.session.modified
        assert client.get("/get").data == b"300"
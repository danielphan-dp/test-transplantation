import flask
import pytest

def test_get_session_value(app, client) -> None:
    @app.route("/set_value", methods=["POST"])
    def set_value() -> str:
        flask.session["value"] = "test_value"
        return ""

    @app.route("/get", methods=["GET"])
    def get_value() -> str:
        return flask.session.get('value', 'None')

    client.post("/set_value")
    response = client.get("/get")
    assert response.data.decode() == "test_value"

def test_get_session_value_default(app, client) -> None:
    response = client.get("/get")
    assert response.data.decode() == "None"

def test_get_session_value_after_clear(app, client) -> None:
    @app.route("/set_value", methods=["POST"])
    def set_value() -> str:
        flask.session["value"] = "test_value"
        return ""

    @app.route("/clear_session", methods=["POST"])
    def clear_session() -> str:
        flask.session.clear()
        return ""

    client.post("/set_value")
    client.post("/clear_session")
    response = client.get("/get")
    assert response.data.decode() == "None"
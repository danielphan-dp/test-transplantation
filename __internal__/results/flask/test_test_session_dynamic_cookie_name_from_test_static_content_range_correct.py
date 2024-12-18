import flask
import pytest

class CustomFlask(flask.Flask):
    pass

@pytest.fixture
def app():
    app = CustomFlask(__name__)
    app.secret_key = "secret_key"
    
    @app.route("/set", methods=["POST"])
    def set():
        flask.session["value"] = flask.request.form["value"]
        return "value set"

    @app.route("/get")
    def get():
        v = flask.session.get("value", "None")
        return v

    return app

@pytest.fixture
def client(app):
    return app.test_client()

def test_get_session_value(client):
    response = client.get("/get")
    assert response.data == b'None'

def test_set_and_get_session_value(client):
    assert client.post("/set", data={"value": "100"}).data == b"value set"
    response = client.get("/get")
    assert response.data == b'100'

def test_get_session_value_after_multiple_sets(client):
    assert client.post("/set", data={"value": "200"}).data == b"value set"
    assert client.post("/set", data={"value": "300"}).data == b"value set"
    response = client.get("/get")
    assert response.data == b'300'

def test_get_session_value_with_no_set(client):
    response = client.get("/get")
    assert response.data == b'None'
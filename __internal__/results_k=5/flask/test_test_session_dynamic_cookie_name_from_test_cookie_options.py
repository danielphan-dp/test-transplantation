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

def test_get_value_set(client):
    client.post("/set", data={"value": "100"})
    response = client.get("/get")
    assert response.data == b"100"

def test_get_value_not_set(client):
    response = client.get("/get")
    assert response.data == b"None"

def test_get_value_after_reset(client):
    client.post("/set", data={"value": "200"})
    client.post("/set", data={"value": "300"})
    response = client.get("/get")
    assert response.data == b"300"

def test_get_value_with_different_session(client):
    with client.session_transaction() as session:
        session['value'] = '400'
    response = client.get("/get")
    assert response.data == b"400"
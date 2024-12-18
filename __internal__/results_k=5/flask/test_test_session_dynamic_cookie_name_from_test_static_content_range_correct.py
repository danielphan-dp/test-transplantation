import flask
import pytest

class CustomFlask(flask.Flask):
    pass

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

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_get_session_value(client):
    response = client.get("/get")
    assert response.data == b'None'

def test_set_and_get_session_value(client):
    assert client.post("/set", data={"value": "100"}).data == b"value set"
    response = client.get("/get")
    assert response.data == b'100'

def test_get_session_value_after_reset(client):
    assert client.post("/set", data={"value": "200"}).data == b"value set"
    client.get("/get")  # Accessing to set the session
    flask.session.clear()  # Simulating session reset
    response = client.get("/get")
    assert response.data == b'None'

def test_get_session_value_with_different_keys(client):
    assert client.post("/set", data={"value": "300"}).data == b"value set"
    response = client.get("/get")
    assert response.data == b'300'
    assert client.post("/set", data={"value": "400"}).data == b"value set"
    response = client.get("/get")
    assert response.data == b'400'
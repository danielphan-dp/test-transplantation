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

def test_get_without_setting_value(client):
    response = client.get("/get")
    assert response.data == b'None'

def test_get_after_setting_value(client):
    client.post("/set", data={"value": "100"})
    response = client.get("/get")
    assert response.data == b'100'

def test_get_with_different_value(client):
    client.post("/set", data={"value": "200"})
    response = client.get("/get")
    assert response.data == b'200'

def test_get_with_empty_value(client):
    client.post("/set", data={"value": ""})
    response = client.get("/get")
    assert response.data == b''

def test_get_with_none_value(client):
    client.post("/set", data={"value": None})
    response = client.get("/get")
    assert response.data == b'None'
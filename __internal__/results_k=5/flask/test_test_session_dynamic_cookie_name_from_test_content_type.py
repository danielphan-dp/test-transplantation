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
    client.post("/set", data={"value": "100"})
    response = client.get("/get")
    assert response.data == b'100'

def test_get_session_value_after_expiration(client):
    client.post("/set", data={"value": "200"})
    # Simulate session expiration
    with client.session_transaction() as sess:
        sess.clear()
    response = client.get("/get")
    assert response.data == b'None'

def test_set_multiple_values(client):
    client.post("/set", data={"value": "300"})
    response = client.get("/get")
    assert response.data == b'300'
    client.post("/set", data={"value": "400"})
    response = client.get("/get")
    assert response.data == b'400'
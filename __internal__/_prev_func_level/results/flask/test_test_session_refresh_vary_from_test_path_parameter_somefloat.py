import flask
import pytest

@pytest.fixture
def client(app):
    return app.test_client()

@app.route("/set_value")
def set_value():
    flask.session["value"] = "test_value"
    return ""

def test_get_value_from_session(client):
    rv = client.get("/set_value")
    assert rv.data == b""

    rv = client.get("/get")
    assert rv.data == b"test_value"

def test_get_value_not_set(client):
    rv = client.get("/get")
    assert rv.data == b'None'
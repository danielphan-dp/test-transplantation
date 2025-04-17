import flask
import pytest

@pytest.fixture
def client(app):
    return app.test_client()

@app.route("/set")
def set_value():
    flask.session['value'] = 'test_value'
    return "Value set"

def test_get_value_none(client):
    rv = client.get('/get')
    assert rv.data == b'None'

def test_get_value_set(client):
    client.get('/set')
    rv = client.get('/get')
    assert rv.data == b'test_value'

def test_get_value_after_reset(client):
    client.get('/set')
    client.get('/get')  # Access to set the session
    flask.session.clear()  # Clear the session
    rv = client.get('/get')
    assert rv.data == b'None'
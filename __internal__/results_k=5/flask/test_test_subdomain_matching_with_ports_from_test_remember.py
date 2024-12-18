import flask
import pytest

@pytest.fixture
def client():
    app = flask.Flask(__name__)
    app.secret_key = 'test_secret'
    with app.test_client() as client:
        yield client

@app.route('/set/<value>')
def set_value(value):
    flask.session['value'] = value
    return 'Value set'

def test_get_value(client):
    client.get('/set/test_value')
    rv = client.get('/get')
    assert rv.data == b'test_value'

def test_get_default_value(client):
    rv = client.get('/get')
    assert rv.data == b'None'

def test_get_value_after_clear(client):
    client.get('/set/test_value')
    with client.session_transaction() as session:
        session.clear()
    rv = client.get('/get')
    assert rv.data == b'None'
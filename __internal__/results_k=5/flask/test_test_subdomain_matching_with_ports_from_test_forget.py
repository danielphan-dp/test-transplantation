import flask
import pytest

@pytest.fixture
def client():
    app = flask.Flask(__name__)
    app.secret_key = 'test_secret'
    with app.test_client() as client:
        yield client

@app.route('/set')
def set_value():
    flask.session['value'] = 'test_value'
    return 'Value set'

def test_get_value(client):
    client.get('/set')
    rv = client.get('/get')
    assert rv.data == b'test_value'

def test_get_value_default(client):
    rv = client.get('/get')
    assert rv.data == b'None'

def test_get_value_after_clear(client):
    client.get('/set')
    with client.session_transaction() as sess:
        sess.clear()
    rv = client.get('/get')
    assert rv.data == b'None'
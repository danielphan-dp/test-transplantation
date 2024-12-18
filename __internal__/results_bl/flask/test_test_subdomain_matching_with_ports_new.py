import flask
import pytest

app = flask.Flask(__name__)

@app.route('/get')
def get():
    v = flask.session.get('value', 'None')
    return v

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_get_value_none(client):
    rv = client.get('/get')
    assert rv.data == b'None'

def test_get_value_set(client):
    with client.session_transaction() as session:
        session['value'] = 'test_value'
    rv = client.get('/get')
    assert rv.data == b'test_value'

def test_get_value_empty_string(client):
    with client.session_transaction() as session:
        session['value'] = ''
    rv = client.get('/get')
    assert rv.data == b''

def test_get_value_nonexistent(client):
    rv = client.get('/get')
    assert rv.data == b'None'
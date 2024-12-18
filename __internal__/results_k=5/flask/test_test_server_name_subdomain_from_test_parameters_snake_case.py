import flask
import pytest

@pytest.fixture
def client():
    app = flask.Flask(__name__)
    with app.test_client() as client:
        yield client

@app.route('/get')
def get():
    v = flask.session.get('value', 'None')
    return v

def test_get_value_none(client):
    rv = client.get('/get')
    assert rv.data == b'None'

def test_get_value_set(client):
    with client.session_transaction() as session:
        session['value'] = 'test_value'
    rv = client.get('/get')
    assert rv.data == b'test_value'

def test_get_value_empty(client):
    with client.session_transaction() as session:
        session['value'] = ''
    rv = client.get('/get')
    assert rv.data == b''

def test_get_value_nonexistent(client):
    rv = client.get('/get')
    assert rv.data == b'None'  # Testing default value when session key does not exist

def test_get_value_overwrite(client):
    with client.session_transaction() as session:
        session['value'] = 'initial_value'
    with client.session_transaction() as session:
        session['value'] = 'overwritten_value'
    rv = client.get('/get')
    assert rv.data == b'overwritten_value'
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

def test_get_default_value(client):
    rv = client.get('/get')
    assert rv.data == b'None'

def test_get_with_value_set(client):
    with client.session_transaction() as session:
        session['value'] = 'test_value'
    rv = client.get('/get')
    assert rv.data == b'test_value'

def test_get_with_none_value(client):
    with client.session_transaction() as session:
        session['value'] = None
    rv = client.get('/get')
    assert rv.data == b'None'

def test_get_with_empty_string(client):
    with client.session_transaction() as session:
        session['value'] = ''
    rv = client.get('/get')
    assert rv.data == b''

def test_get_with_numeric_value(client):
    with client.session_transaction() as session:
        session['value'] = 123
    rv = client.get('/get')
    assert rv.data == b'123'
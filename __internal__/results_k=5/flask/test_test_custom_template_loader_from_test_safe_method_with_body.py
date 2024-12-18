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

def test_get_with_default_value(client):
    response = client.get('/get')
    assert response.data == b'None'

def test_get_with_set_value(client):
    with client.session_transaction() as session:
        session['value'] = 'Test Value'
    response = client.get('/get')
    assert response.data == b'Test Value'

def test_get_with_empty_value(client):
    with client.session_transaction() as session:
        session['value'] = ''
    response = client.get('/get')
    assert response.data == b''

def test_get_with_none_value(client):
    with client.session_transaction() as session:
        session['value'] = None
    response = client.get('/get')
    assert response.data == b'None'
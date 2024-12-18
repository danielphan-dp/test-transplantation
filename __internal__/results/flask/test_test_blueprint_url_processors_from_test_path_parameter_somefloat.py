import pytest
import flask
from blueprintapp.app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_get_session_value_none(client):
    response = client.get('/get')
    assert response.data == b'None'

def test_get_session_value_set(client):
    with client.session_transaction() as session:
        session['value'] = 'test_value'
    response = client.get('/get')
    assert response.data == b'test_value'

def test_get_session_value_empty_string(client):
    with client.session_transaction() as session:
        session['value'] = ''
    response = client.get('/get')
    assert response.data == b''

def test_get_session_value_nonexistent(client):
    response = client.get('/get')
    assert response.data == b'None'  # Testing default value when session key does not exist

def test_get_session_value_overwrite(client):
    with client.session_transaction() as session:
        session['value'] = 'initial_value'
    with client.session_transaction() as session:
        session['value'] = 'overwritten_value'
    response = client.get('/get')
    assert response.data == b'overwritten_value'
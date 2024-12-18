import pytest
import flask
from blueprintapp.app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_get_value_none(client):
    response = client.get('/get')
    assert response.data == b'None'

def test_get_value_set(client):
    with client.session_transaction() as session:
        session['value'] = 'Test Value'
    response = client.get('/get')
    assert response.data == b'Test Value'

def test_get_value_empty_string(client):
    with client.session_transaction() as session:
        session['value'] = ''
    response = client.get('/get')
    assert response.data == b''

def test_get_value_nonexistent_key(client):
    response = client.get('/get')
    assert response.data == b'None'
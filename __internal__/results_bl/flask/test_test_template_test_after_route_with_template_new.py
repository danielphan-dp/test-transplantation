import pytest
import flask
from blueprintapp.app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_get_value_from_session(client):
    with client.session_transaction() as session:
        session['value'] = 'Test Value'
    response = client.get('/get')
    assert response.data == b'Test Value'

def test_get_value_not_set(client):
    response = client.get('/get')
    assert response.data == b'None'

def test_get_value_set_to_none(client):
    with client.session_transaction() as session:
        session['value'] = None
    response = client.get('/get')
    assert response.data == b'None'

def test_get_value_set_to_boolean(client):
    with client.session_transaction() as session:
        session['value'] = True
    response = client.get('/get')
    assert response.data == b'True'

def test_get_value_set_to_empty_string(client):
    with client.session_transaction() as session:
        session['value'] = ''
    response = client.get('/get')
    assert response.data == b''
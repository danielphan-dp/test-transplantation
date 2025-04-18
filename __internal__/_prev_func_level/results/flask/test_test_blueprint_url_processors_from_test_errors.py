import pytest
import flask
from blueprintapp.app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_get_value_from_session(client):
    with client.session_transaction() as session:
        session['value'] = 'test_value'
    
    response = client.get('/get')
    assert response.data == b'test_value'

def test_get_value_not_set(client):
    response = client.get('/get')
    assert response.data == b'None'

def test_get_value_empty_string(client):
    with client.session_transaction() as session:
        session['value'] = ''
    
    response = client.get('/get')
    assert response.data == b''

def test_get_value_none(client):
    with client.session_transaction() as session:
        session['value'] = None
    
    response = client.get('/get')
    assert response.data == b'None'
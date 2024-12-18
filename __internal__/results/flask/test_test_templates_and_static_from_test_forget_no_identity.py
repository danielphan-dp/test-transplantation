import pytest
import flask
from blueprintapp import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_get_session_value(client):
    with client.session_transaction() as session:
        session['value'] = 'Test Value'
    
    rv = client.get('/get')
    assert rv.data == b'Test Value'

def test_get_session_value_default(client):
    rv = client.get('/get')
    assert rv.data == b'None'

def test_get_session_value_empty(client):
    with client.session_transaction() as session:
        session['value'] = ''
    
    rv = client.get('/get')
    assert rv.data == b''

def test_get_session_value_none(client):
    with client.session_transaction() as session:
        session['value'] = None
    
    rv = client.get('/get')
    assert rv.data == b'None'
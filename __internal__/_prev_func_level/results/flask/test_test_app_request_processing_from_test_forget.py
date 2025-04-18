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

def test_get_session_value_empty(client):
    with client.session_transaction() as session:
        session['value'] = ''
    response = client.get('/get')
    assert response.data == b''

def test_get_session_value_after_teardown(client):
    with client.session_transaction() as session:
        session['value'] = 'value_before_teardown'
    response = client.get('/get')
    assert response.data == b'value_before_teardown'
    
    with client.session_transaction() as session:
        session.clear()
    response_after_teardown = client.get('/get')
    assert response_after_teardown.data == b'None'
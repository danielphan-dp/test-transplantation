import pytest
import flask
from blueprintapp.app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_get_value_from_session(client):
    with client.session_transaction() as session:
        session['value'] = 'test_value'
    response = client.get('/get')
    assert response.data == b'test_value'

def test_get_value_from_empty_session(client):
    response = client.get('/get')
    assert response.data == b'None'

def test_get_value_from_session_none(client):
    with client.session_transaction() as session:
        session['value'] = None
    response = client.get('/get')
    assert response.data == b'None'
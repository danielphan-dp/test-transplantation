import pytest
import flask
from blueprintapp.app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_get_route_with_default_value(client):
    response = client.get('/get')
    assert response.data == b'None'

def test_get_route_with_session_value(client):
    with client.session_transaction() as session:
        session['value'] = 'test_value'
    response = client.get('/get')
    assert response.data == b'test_value'

def test_get_route_with_empty_session(client):
    response = client.get('/get')
    assert response.data == b'None'
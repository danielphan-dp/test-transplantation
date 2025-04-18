import pytest
import flask

@pytest.fixture
def client(app):
    return app.test_client()

def test_get_value_from_session(client):
    with client.session_transaction() as session:
        session['value'] = 'Test Value'
    response = client.get('/get')
    assert response.data == b'Test Value'

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
import pytest
import flask

@pytest.fixture
def client(app):
    return app.test_client()

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

def test_get_session_value_none_type(client):
    with client.session_transaction() as session:
        session['value'] = None
    response = client.get('/get')
    assert response.data == b'None'  # Testing None value in session
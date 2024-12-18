import flask
import pytest

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

def test_get_session_value_empty(client):
    with client.session_transaction() as session:
        session['value'] = ''
    response = client.get('/get')
    assert response.data == b''

def test_get_session_value_nonexistent(client):
    response = client.get('/get')
    assert response.data == b'None'  # Ensure it defaults to 'None' if not set

def test_get_session_value_after_clear(client):
    with client.session_transaction() as session:
        session['value'] = 'test_value'
    with client.session_transaction() as session:
        session.clear()
    response = client.get('/get')
    assert response.data == b'None'  # Ensure it defaults to 'None' after clearing session
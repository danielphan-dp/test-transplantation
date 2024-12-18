import flask
import pytest

@pytest.fixture
def client(app):
    return app.test_client()

def test_get_session_value_none(client):
    rv = client.get('/get')
    assert rv.data == b'None'

def test_get_session_value_set(client):
    with client.session_transaction() as session:
        session['value'] = 'Test Value'
    rv = client.get('/get')
    assert rv.data == b'Test Value'

def test_get_session_value_empty(client):
    with client.session_transaction() as session:
        session['value'] = ''
    rv = client.get('/get')
    assert rv.data == b''

def test_get_session_value_nonexistent(client):
    rv = client.get('/get')
    assert rv.data == b'None'  # Testing default value when session key does not exist

def test_get_session_value_overwrite(client):
    with client.session_transaction() as session:
        session['value'] = 'Initial Value'
    with client.session_transaction() as session:
        session['value'] = 'Overwritten Value'
    rv = client.get('/get')
    assert rv.data == b'Overwritten Value'
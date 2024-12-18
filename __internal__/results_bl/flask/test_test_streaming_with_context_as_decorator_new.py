import flask
import pytest

@pytest.fixture
def client(app):
    return app.test_client()

def test_get_value_from_session(client):
    with client.session_transaction() as session:
        session['value'] = 'TestValue'
    rv = client.get('/get')
    assert rv.data == b'TestValue'

def test_get_value_not_set(client):
    rv = client.get('/get')
    assert rv.data == b'None'

def test_get_value_empty_string(client):
    with client.session_transaction() as session:
        session['value'] = ''
    rv = client.get('/get')
    assert rv.data == b''

def test_get_value_none(client):
    with client.session_transaction() as session:
        session['value'] = None
    rv = client.get('/get')
    assert rv.data == b'None'
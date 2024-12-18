import flask
import pytest

@pytest.fixture
def client(app):
    return app.test_client()

def test_get_session_value_none(client):
    rv = client.get('/get')
    assert rv.status_code == 200
    assert rv.data == b'None'

def test_get_session_value_set(client):
    with client.session_transaction() as session:
        session['value'] = 'TestValue'
    rv = client.get('/get')
    assert rv.status_code == 200
    assert rv.data == b'TestValue'

def test_get_session_value_empty(client):
    with client.session_transaction() as session:
        session['value'] = ''
    rv = client.get('/get')
    assert rv.status_code == 200
    assert rv.data == b''

def test_get_session_value_nonexistent(client):
    rv = client.get('/get')
    assert rv.status_code == 200
    assert rv.data == b'None'
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
        session['value'] = 'test_value'
    rv = client.get('/get')
    assert rv.status_code == 200
    assert rv.data == b'test_value'

def test_get_session_value_empty(client):
    with client.session_transaction() as session:
        session['value'] = ''
    rv = client.get('/get')
    assert rv.status_code == 200
    assert rv.data == b''

def test_get_session_value_overwrite(client):
    with client.session_transaction() as session:
        session['value'] = 'initial_value'
    with client.session_transaction() as session:
        session['value'] = 'new_value'
    rv = client.get('/get')
    assert rv.status_code == 200
    assert rv.data == b'new_value'
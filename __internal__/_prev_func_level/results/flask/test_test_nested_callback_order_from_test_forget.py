import flask
import pytest

@pytest.fixture
def client(app):
    return app.test_client()

def test_get_value_none(client):
    response = client.get('/get')
    assert response.data == b'None'

def test_get_value_set(client):
    with client.session_transaction() as session:
        session['value'] = 'test_value'
    response = client.get('/get')
    assert response.data == b'test_value'

def test_get_value_empty(client):
    with client.session_transaction() as session:
        session['value'] = ''
    response = client.get('/get')
    assert response.data == b''

def test_get_value_overwrite(client):
    with client.session_transaction() as session:
        session['value'] = 'initial_value'
    with client.session_transaction() as session:
        session['value'] = 'new_value'
    response = client.get('/get')
    assert response.data == b'new_value'
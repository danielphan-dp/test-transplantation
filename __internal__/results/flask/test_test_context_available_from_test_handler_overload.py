import flask
import pytest

@pytest.fixture
def client(app):
    return app.test_client()

def test_get_value_from_session(client):
    with flask.session_transaction() as session:
        session['value'] = 'test_value'
    response = client.get('/get')
    assert response.data == b'test_value'

def test_get_value_not_set(client):
    response = client.get('/get')
    assert response.data == b'None'

def test_get_value_empty_string(client):
    with flask.session_transaction() as session:
        session['value'] = ''
    response = client.get('/get')
    assert response.data == b''

def test_get_value_none(client):
    with flask.session_transaction() as session:
        session['value'] = None
    response = client.get('/get')
    assert response.data == b'None'
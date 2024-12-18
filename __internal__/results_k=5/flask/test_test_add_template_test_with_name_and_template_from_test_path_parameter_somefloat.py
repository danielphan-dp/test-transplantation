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
        session['value'] = 'Test Value'
    response = client.get('/get')
    assert response.data == b'Test Value'

def test_get_session_value_empty_string(client):
    with client.session_transaction() as session:
        session['value'] = ''
    response = client.get('/get')
    assert response.data == b''

def test_get_session_value_nonexistent(client):
    response = client.get('/get')
    assert response.data == b'None'  # Testing default value when session key does not exist

def test_get_session_value_boolean(client):
    with client.session_transaction() as session:
        session['value'] = True
    response = client.get('/get')
    assert response.data == b'True'  # Testing boolean value in session

def test_get_session_value_integer(client):
    with client.session_transaction() as session:
        session['value'] = 42
    response = client.get('/get')
    assert response.data == b'42'  # Testing integer value in session

def test_get_session_value_float(client):
    with client.session_transaction() as session:
        session['value'] = 3.14
    response = client.get('/get')
    assert response.data == b'3.14'  # Testing float value in session
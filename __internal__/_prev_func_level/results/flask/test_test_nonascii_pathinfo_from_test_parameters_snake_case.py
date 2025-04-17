import flask
import pytest

@pytest.fixture
def client(app):
    return app.test_client()

def test_get_session_value(client):
    with client.session_transaction() as session:
        session['value'] = 'test_value'
    
    rv = client.get('/get')
    assert rv.data == b'test_value'

def test_get_session_value_default(client):
    rv = client.get('/get')
    assert rv.data == b'None'

def test_get_session_value_nonascii(client):
    with client.session_transaction() as session:
        session['value'] = 'тестовое значение'
    
    rv = client.get('/get')
    assert rv.data == b'\xd1\x82\xd0\xb5\xd1\x81\xd1\x82\xd0\xbe\xd0\xb2\xd0\xbe\xd0\xb5 \xd0\xb7\xd0\xbd\xd0\xb0\xd1\x87\xd0\xb5\xd0\xbd\xd0\xb8\xd0\xb5'  # Non-ASCII bytes representation

def test_get_session_value_empty(client):
    with client.session_transaction() as session:
        session['value'] = ''
    
    rv = client.get('/get')
    assert rv.data == b''
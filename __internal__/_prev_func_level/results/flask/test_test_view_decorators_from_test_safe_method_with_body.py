import flask
import pytest

@pytest.fixture
def client(app):
    return app.test_client()

def test_get_value_from_session(client):
    with client.session_transaction() as session:
        session['value'] = 'Test Value'
    
    rv = client.get('/get')
    assert rv.data.decode('utf-8') == 'Test Value'

def test_get_value_not_set(client):
    rv = client.get('/get')
    assert rv.data.decode('utf-8') == 'None'

def test_get_value_empty_string(client):
    with client.session_transaction() as session:
        session['value'] = ''
    
    rv = client.get('/get')
    assert rv.data.decode('utf-8') == ''
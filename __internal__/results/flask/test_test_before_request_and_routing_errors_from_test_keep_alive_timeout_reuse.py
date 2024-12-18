import flask
import pytest

@pytest.fixture
def client(app):
    return app.test_client()

def test_get_value_from_session(client):
    with client.session_transaction() as session:
        session['value'] = 'test_value'
    
    rv = client.get('/get')
    assert rv.data == b'test_value'

def test_get_value_not_set(client):
    rv = client.get('/get')
    assert rv.data == b'None'

def test_get_value_after_modification(client):
    with client.session_transaction() as session:
        session['value'] = 'initial_value'
    
    rv = client.get('/get')
    assert rv.data == b'initial_value'
    
    with client.session_transaction() as session:
        session['value'] = 'modified_value'
    
    rv = client.get('/get')
    assert rv.data == b'modified_value'
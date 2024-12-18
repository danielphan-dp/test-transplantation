import flask
import pytest

def test_get_value_from_session(app, client):
    with client.session_transaction() as session:
        session['value'] = 'Test Value'
    
    rv = client.get('/get')
    assert rv.data == b'Test Value'

def test_get_value_from_session_default(app, client):
    rv = client.get('/get')
    assert rv.data == b'None'

def test_get_value_from_session_empty(app, client):
    with client.session_transaction() as session:
        session.clear()
    
    rv = client.get('/get')
    assert rv.data == b'None'
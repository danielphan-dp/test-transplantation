import flask
import pytest

def test_get_value_from_session(app, client):
    with client.session_transaction() as session:
        session['value'] = 'test_value'
    
    rv = client.get('/get')
    assert rv.data == b'test_value'

def test_get_value_not_set(app, client):
    rv = client.get('/get')
    assert rv.data == b'None'

def test_get_value_after_clear_session(app, client):
    with client.session_transaction() as session:
        session['value'] = 'test_value'
    
    with client.session_transaction() as session:
        session.clear()
    
    rv = client.get('/get')
    assert rv.data == b'None'
import flask
import pytest

def test_get_value_from_session(app, client):
    with client.session_transaction() as session:
        session['value'] = 'test_value'
    
    rv = client.get('/get')
    assert rv.data == b'test_value'

def test_get_value_from_empty_session(app, client):
    rv = client.get('/get')
    assert rv.data == b'None'

def test_get_value_from_session_after_modification(app, client):
    with client.session_transaction() as session:
        session['value'] = 'initial_value'
    
    rv = client.get('/get')
    assert rv.data == b'initial_value'
    
    with client.session_transaction() as session:
        session['value'] = 'modified_value'
    
    rv = client.get('/get')
    assert rv.data == b'modified_value'

def test_get_value_from_session_with_none_value(app, client):
    with client.session_transaction() as session:
        session['value'] = None
    
    rv = client.get('/get')
    assert rv.data == b'None'
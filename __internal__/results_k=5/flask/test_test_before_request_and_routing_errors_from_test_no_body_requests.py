import flask
import pytest

def test_get_method_with_session_value(app, client):
    with client.session_transaction() as session:
        session['value'] = 'test_value'
    
    rv = client.get('/get')
    assert rv.data == b'test_value'

def test_get_method_with_no_session_value(app, client):
    rv = client.get('/get')
    assert rv.data == b'None'

def test_get_method_with_empty_session_value(app, client):
    with client.session_transaction() as session:
        session['value'] = ''
    
    rv = client.get('/get')
    assert rv.data == b''
import flask
import pytest

def test_get_session_value(app, client):
    with client.session_transaction() as session:
        session['value'] = 'test_value'
    
    rv = client.get('/get')
    assert rv.data.decode('utf-8') == 'test_value'

def test_get_session_value_default(app, client):
    rv = client.get('/get')
    assert rv.data.decode('utf-8') == 'None'

def test_get_session_value_empty(app, client):
    with client.session_transaction() as session:
        session['value'] = ''
    
    rv = client.get('/get')
    assert rv.data.decode('utf-8') == ''
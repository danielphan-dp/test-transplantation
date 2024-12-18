import flask
import pytest

def test_get_value_from_session(app, client):
    with client.session_transaction() as session:
        session['value'] = 'test_value'
    
    rv = client.get('/get')
    assert rv.data.decode('utf-8') == 'test_value'

def test_get_value_not_set(app, client):
    rv = client.get('/get')
    assert rv.data.decode('utf-8') == 'None'

def test_get_value_empty_string(app, client):
    with client.session_transaction() as session:
        session['value'] = ''
    
    rv = client.get('/get')
    assert rv.data.decode('utf-8') == '' 

def test_get_value_none(app, client):
    with client.session_transaction() as session:
        session['value'] = None
    
    rv = client.get('/get')
    assert rv.data.decode('utf-8') == 'None'
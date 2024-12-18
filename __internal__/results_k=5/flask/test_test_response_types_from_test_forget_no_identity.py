import flask
import pytest

def test_get_value_from_session(app, client):
    with client.session_transaction() as session:
        session['value'] = 'Test Value'
    
    rv = client.get('/get')
    assert rv.data.decode() == 'Test Value'

def test_get_value_not_set(app, client):
    rv = client.get('/get')
    assert rv.data.decode() == 'None'

def test_get_value_empty_string(app, client):
    with client.session_transaction() as session:
        session['value'] = ''
    
    rv = client.get('/get')
    assert rv.data.decode() == ''
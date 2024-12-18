import flask
import pytest

def test_get_value_from_session(app, client):
    with client.session_transaction() as session:
        session['value'] = 'test_value'
    
    rv = client.get('/get')
    assert rv.data.decode() == 'test_value'

def test_get_value_not_set_in_session(app, client):
    rv = client.get('/get')
    assert rv.data.decode() == 'None'

def test_get_value_with_none_in_session(app, client):
    with client.session_transaction() as session:
        session['value'] = None
    
    rv = client.get('/get')
    assert rv.data.decode() == 'None'
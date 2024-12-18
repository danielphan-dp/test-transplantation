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

def test_get_value_after_setting(app, client):
    with client.session_transaction() as session:
        session['value'] = 'another_value'
    
    rv = client.get('/get')
    assert rv.data == b'another_value'

def test_get_value_with_empty_session(app, client):
    with client.session_transaction() as session:
        session.clear()
    
    rv = client.get('/get')
    assert rv.data == b'None'
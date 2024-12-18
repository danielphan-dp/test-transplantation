import flask
import pytest

def test_get_value_from_session(app, client):
    with client.session_transaction() as session:
        session['value'] = 'TestValue'
    
    rv = client.get('/get')
    assert rv.data == b'TestValue'

def test_get_value_not_set_in_session(app, client):
    rv = client.get('/get')
    assert rv.data == b'None'

def test_get_value_with_different_session_value(app, client):
    with client.session_transaction() as session:
        session['value'] = 'AnotherValue'
    
    rv = client.get('/get')
    assert rv.data == b'AnotherValue'

def test_get_value_after_session_clear(app, client):
    with client.session_transaction() as session:
        session['value'] = 'ValueBeforeClear'
    
    with client.session_transaction() as session:
        session.clear()
    
    rv = client.get('/get')
    assert rv.data == b'None'
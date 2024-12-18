import flask
import pytest

def test_get_value_from_session(app, client):
    with client.session_transaction() as session:
        session['value'] = 'Test Value'
    
    rv = client.get('/get')
    assert rv.data == b'Test Value'

def test_get_value_not_set_in_session(app, client):
    rv = client.get('/get')
    assert rv.data == b'None'

def test_get_value_with_different_session_value(app, client):
    with client.session_transaction() as session:
        session['value'] = 'Another Value'
    
    rv = client.get('/get')
    assert rv.data == b'Another Value'

def test_get_value_after_session_clear(app, client):
    with client.session_transaction() as session:
        session['value'] = 'Value Before Clear'
    
    with client.session_transaction() as session:
        session.clear()
    
    rv = client.get('/get')
    assert rv.data == b'None'
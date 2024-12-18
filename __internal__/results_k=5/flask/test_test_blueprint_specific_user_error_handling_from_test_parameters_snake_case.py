import flask
import pytest

def test_get_value_from_session(app, client):
    with client.session_transaction() as session:
        session['value'] = 'test_value'
    
    response = client.get('/get')
    assert response.data == b'test_value'

def test_get_value_from_session_default(app, client):
    response = client.get('/get')
    assert response.data == b'None'

def test_get_value_from_session_empty(app, client):
    with client.session_transaction() as session:
        session.clear()
    
    response = client.get('/get')
    assert response.data == b'None'
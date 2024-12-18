import flask
import pytest

def test_get_value_from_session(app, client):
    with client.session_transaction() as session:
        session['value'] = 'test_value'
    
    response = client.get('/get')
    assert response.data == b'test_value'

def test_get_value_not_set(app, client):
    response = client.get('/get')
    assert response.data == b'None'

def test_get_value_after_clear_session(app, client):
    with client.session_transaction() as session:
        session['value'] = 'test_value'
    
    with client.session_transaction() as session:
        session.clear()
    
    response = client.get('/get')
    assert response.data == b'None'

def test_get_value_multiple_sessions(app, client):
    with client.session_transaction() as session1:
        session1['value'] = 'session1_value'
    
    response1 = client.get('/get')
    assert response1.data == b'session1_value'
    
    with client.session_transaction() as session2:
        session2['value'] = 'session2_value'
    
    response2 = client.get('/get')
    assert response2.data == b'session2_value'
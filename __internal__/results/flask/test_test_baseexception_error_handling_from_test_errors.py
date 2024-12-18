import pytest
import flask

def test_get_value_from_session(app, client):
    with client.session_transaction() as session:
        session['value'] = 'test_value'
    
    response = client.get('/get')
    assert response.data.decode() == 'test_value'

def test_get_value_not_set_in_session(app, client):
    response = client.get('/get')
    assert response.data.decode() == 'None'

def test_get_value_with_empty_session(app, client):
    with client.session_transaction() as session:
        session.clear()
    
    response = client.get('/get')
    assert response.data.decode() == 'None'

def test_get_value_after_session_expiration(app, client):
    with client.session_transaction() as session:
        session['value'] = 'temporary_value'
        session.permanent = True
    
    response = client.get('/get')
    assert response.data.decode() == 'temporary_value'
    
    with client.session_transaction() as session:
        session.clear()
    
    response_after_expiration = client.get('/get')
    assert response_after_expiration.data.decode() == 'None'
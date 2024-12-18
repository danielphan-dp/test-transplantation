import flask
import pytest

def test_get_value_from_session(app, client):
    with client.session_transaction() as session:
        session['value'] = 'test_value'
    
    response = client.get('/get')
    assert response.data.decode() == 'test_value'

def test_get_value_not_set_in_session(app, client):
    response = client.get('/get')
    assert response.data.decode() == 'None'

def test_get_value_after_modification(app, client):
    with client.session_transaction() as session:
        session['value'] = 'initial_value'
    
    response = client.get('/get')
    assert response.data.decode() == 'initial_value'
    
    with client.session_transaction() as session:
        session['value'] = 'modified_value'
    
    response = client.get('/get')
    assert response.data.decode() == 'modified_value'
import pytest
import flask

def test_get_value_from_session(app, client):
    with client.session_transaction() as session:
        session['value'] = 'test_value'
    
    response = client.get('/get')
    assert response.data.decode() == 'test_value'
    assert response.status_code == 200

def test_get_value_not_set_in_session(app, client):
    response = client.get('/get')
    assert response.data.decode() == 'None'
    assert response.status_code == 200

def test_get_value_with_different_session_data(app, client):
    with client.session_transaction() as session:
        session['value'] = 'another_value'
    
    response = client.get('/get')
    assert response.data.decode() == 'another_value'
    assert response.status_code == 200

def test_get_value_after_session_clear(app, client):
    with client.session_transaction() as session:
        session['value'] = 'value_before_clear'
    
    with client.session_transaction() as session:
        session.clear()
    
    response = client.get('/get')
    assert response.data.decode() == 'None'
    assert response.status_code == 200

def test_get_value_with_multiple_keys(app, client):
    with client.session_transaction() as session:
        session['value'] = 'value1'
        session['other_key'] = 'value2'
    
    response = client.get('/get')
    assert response.data.decode() == 'value1'
    assert response.status_code == 200

def test_get_value_with_empty_session(app, client):
    response = client.get('/get')
    assert response.data.decode() == 'None'
    assert response.status_code == 200
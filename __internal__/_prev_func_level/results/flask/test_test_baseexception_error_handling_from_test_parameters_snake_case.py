import pytest
import flask

def test_get_value_from_session(app, client):
    app.testing = True
    with client.session_transaction() as session:
        session['value'] = 'test_value'
    
    response = client.get('/get')
    assert response.data.decode() == 'test_value'

def test_get_value_not_set(app, client):
    app.testing = True
    response = client.get('/get')
    assert response.data.decode() == 'None'

def test_get_value_with_none(app, client):
    app.testing = True
    with client.session_transaction() as session:
        session['value'] = None
    
    response = client.get('/get')
    assert response.data.decode() == 'None'

def test_get_value_with_empty_string(app, client):
    app.testing = True
    with client.session_transaction() as session:
        session['value'] = ''
    
    response = client.get('/get')
    assert response.data.decode() == ''
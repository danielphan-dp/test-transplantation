import flask
import pytest

def test_get_value_from_session(app, client):
    app.testing = True
    with client.session_transaction() as session:
        session['value'] = 'test_value'
    
    response = client.get('/get')
    assert response.data == b'test_value'

def test_get_value_not_set_in_session(app, client):
    app.testing = True
    response = client.get('/get')
    assert response.data == b'None'

def test_get_value_with_none_in_session(app, client):
    app.testing = True
    with client.session_transaction() as session:
        session['value'] = None
    
    response = client.get('/get')
    assert response.data == b'None'
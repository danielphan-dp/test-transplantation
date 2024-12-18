import pytest
import flask

def test_get_value_from_session(app, client):
    """Test retrieving value from session."""
    
    with client.session_transaction() as session:
        session['value'] = 'test_value'
    
    response = client.get('/get')
    assert response.data == b'test_value'

def test_get_value_from_session_default(app, client):
    """Test retrieving default value when session key does not exist."""
    
    response = client.get('/get')
    assert response.data == b'None'

def test_get_value_from_session_empty(app, client):
    """Test retrieving empty value from session."""
    
    with client.session_transaction() as session:
        session['value'] = ''
    
    response = client.get('/get')
    assert response.data == b''

def test_get_value_from_session_none(app, client):
    """Test retrieving None value from session."""
    
    with client.session_transaction() as session:
        session['value'] = None
    
    response = client.get('/get')
    assert response.data == b'None'
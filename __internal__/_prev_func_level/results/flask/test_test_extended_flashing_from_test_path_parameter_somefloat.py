import flask
import pytest

def test_get_value_from_session(app):
    client = app.test_client()
    
    # Test default value when session is empty
    response = client.get('/get')
    assert response.data.decode() == 'None'
    
    # Test setting a value in the session
    with client.session_transaction() as session:
        session['value'] = 'Test Value'
    
    # Test retrieving the value from session
    response = client.get('/get')
    assert response.data.decode() == 'Test Value'

def test_get_value_with_nonexistent_key(app):
    client = app.test_client()
    
    # Test retrieving a nonexistent key
    response = client.get('/get')
    assert response.data.decode() == 'None'  # Ensure it returns 'None' for nonexistent key

def test_get_value_after_clearing_session(app):
    client = app.test_client()
    
    # Set a value in the session
    with client.session_transaction() as session:
        session['value'] = 'Another Value'
    
    # Clear the session
    with client.session_transaction() as session:
        session.clear()
    
    # Test retrieving the value after clearing session
    response = client.get('/get')
    assert response.data.decode() == 'None'  # Ensure it returns 'None' after clearing session
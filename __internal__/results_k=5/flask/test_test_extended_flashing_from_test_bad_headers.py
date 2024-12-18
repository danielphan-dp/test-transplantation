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

def test_get_value_with_no_session(app):
    client = app.test_client()

    # Ensure no session value is set
    response = client.get('/get')
    assert response.data.decode() == 'None'

def test_get_value_after_session_clear(app):
    client = app.test_client()

    # Set a value in the session
    with client.session_transaction() as session:
        session['value'] = 'Another Value'
    
    # Clear the session
    with client.session_transaction() as session:
        session.clear()

    # Test retrieving the value after clearing the session
    response = client.get('/get')
    assert response.data.decode() == 'None'
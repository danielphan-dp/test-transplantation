import pytest
import flask

def test_get_value_from_session(app, client):
    """Test retrieving value from session."""
    with client.session_transaction() as session:
        session['value'] = 'test_value'
    response = client.get('/get')
    assert response.data == b'test_value'

def test_get_value_not_set(app, client):
    """Test retrieving value when session value is not set."""
    response = client.get('/get')
    assert response.data == b'None'

def test_get_value_empty_string(app, client):
    """Test retrieving empty string from session."""
    with client.session_transaction() as session:
        session['value'] = ''
    response = client.get('/get')
    assert response.data == b''

def test_get_value_none_type(app, client):
    """Test retrieving None type from session."""
    with client.session_transaction() as session:
        session['value'] = None
    response = client.get('/get')
    assert response.data == b'None'
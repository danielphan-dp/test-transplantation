import pytest
import flask

@pytest.fixture
def client(app):
    return app.test_client()

def test_get_session_value(client):
    """Test the /get route to ensure it returns the correct session value."""
    with client.session_transaction() as session:
        session['value'] = 'test_value'
    
    response = client.get('/get')
    assert response.data == b'test_value'

def test_get_session_value_none(client):
    """Test the /get route when session value is not set."""
    response = client.get('/get')
    assert response.data == b'None'

def test_get_session_value_empty(client):
    """Test the /get route when session value is set to an empty string."""
    with client.session_transaction() as session:
        session['value'] = ''
    
    response = client.get('/get')
    assert response.data == b''
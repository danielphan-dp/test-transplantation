import pytest
import flask

@pytest.fixture
def client(app):
    return app.test_client()

def test_get_session_value_none(client):
    """Test that the default value is returned when no session value is set."""
    response = client.get('/get')
    assert response.data == b'None'

def test_get_session_value_set(client):
    """Test that the correct session value is returned when it is set."""
    with client.session_transaction() as session:
        session['value'] = 'test_value'
    response = client.get('/get')
    assert response.data == b'test_value'

def test_get_session_value_empty_string(client):
    """Test that an empty string is returned when the session value is set to an empty string."""
    with client.session_transaction() as session:
        session['value'] = ''
    response = client.get('/get')
    assert response.data == b''

def test_get_session_value_none_type(client):
    """Test that None is returned when the session value is explicitly set to None."""
    with client.session_transaction() as session:
        session['value'] = None
    response = client.get('/get')
    assert response.data == b'None'
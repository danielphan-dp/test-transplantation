import pytest
import flask

def test_get_value_none(self, app, client):
    """Test the /get endpoint when session value is not set."""
    with client.session_transaction() as session:
        session['value'] = None
    response = client.get('/get')
    assert response.data == b'None'

def test_get_value_set(self, app, client):
    """Test the /get endpoint when session value is set."""
    with client.session_transaction() as session:
        session['value'] = 'test_value'
    response = client.get('/get')
    assert response.data == b'test_value'

def test_get_value_default(self, app, client):
    """Test the /get endpoint when session value is not set, expecting default."""
    response = client.get('/get')
    assert response.data == b'None'

def test_get_value_empty_string(self, app, client):
    """Test the /get endpoint when session value is an empty string."""
    with client.session_transaction() as session:
        session['value'] = ''
    response = client.get('/get')
    assert response.data == b''

def test_get_value_integer(self, app, client):
    """Test the /get endpoint when session value is an integer."""
    with client.session_transaction() as session:
        session['value'] = 42
    response = client.get('/get')
    assert response.data == b'42'
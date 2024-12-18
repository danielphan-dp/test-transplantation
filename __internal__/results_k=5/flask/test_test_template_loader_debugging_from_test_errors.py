import flask
import pytest

def test_get_value_from_session(app, client):
    with app.test_client() as c:
        # Test default value when session is empty
        response = c.get('/get')
        assert response.data.decode() == 'None'
        
        # Test setting a value in the session
        with c.session_transaction() as sess:
            sess['value'] = 'test_value'
        
        # Test retrieving the value from session
        response = c.get('/get')
        assert response.data.decode() == 'test_value'

def test_get_value_with_nonexistent_key(app, client):
    with app.test_client() as c:
        # Ensure that accessing a nonexistent key returns 'None'
        response = c.get('/get')
        assert response.data.decode() == 'None'
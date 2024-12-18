import flask
import pytest

def test_get_value_from_session(app):
    with app.test_client() as client:
        # Test default value when session is empty
        response = client.get('/get')
        assert response.data.decode() == 'None'

        # Test setting a value in the session
        with flask.session_transaction() as session:
            session['value'] = 'Test Value'
        
        # Test retrieving the value from session
        response = client.get('/get')
        assert response.data.decode() == 'Test Value'

def test_get_value_with_no_session(app):
    with app.test_client() as client:
        # Ensure no session value is set
        response = client.get('/get')
        assert response.data.decode() == 'None'
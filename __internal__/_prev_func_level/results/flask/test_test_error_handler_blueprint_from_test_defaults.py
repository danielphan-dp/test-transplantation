import pytest
import flask

def test_get_value_from_session(app):
    with app.test_client() as c:
        # Test default value when session is empty
        response = c.get('/get')
        assert response.data == b'None'

        # Test setting a value in the session
        with app.app_context():
            flask.session['value'] = 'test_value'
        
        # Test retrieving the value from session
        response = c.get('/get')
        assert response.data == b'test_value'

def test_get_value_with_no_session(app):
    with app.test_client() as c:
        # Ensure session is not set
        with app.app_context():
            flask.session.clear()
        
        response = c.get('/get')
        assert response.data == b'None'
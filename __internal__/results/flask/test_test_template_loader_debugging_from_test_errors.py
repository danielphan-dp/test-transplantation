import flask
import pytest

def test_get_value_from_session(app, client):
    with app.test_client() as c:
        # Test default value when session is empty
        response = c.get('/get')
        assert response.data.decode() == 'None'
        
        # Test setting a value in the session
        with flask.session_transaction() as session:
            session['value'] = 'test_value'
        
        # Test retrieving the value from session
        response = c.get('/get')
        assert response.data.decode() == 'test_value'

def test_get_value_from_session_with_no_value(app, client):
    with app.test_client() as c:
        # Ensure session does not have 'value'
        with flask.session_transaction() as session:
            session.clear()
        
        response = c.get('/get')
        assert response.data.decode() == 'None'
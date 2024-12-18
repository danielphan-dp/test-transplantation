import flask
import pytest

def test_get_value_from_session(app, client):
    with client:
        # Test default value when session is empty
        response = client.get('/get')
        assert response.data == b'None'

        # Test setting a value in the session
        with flask.session_transaction() as session:
            session['value'] = 'test_value'
        
        # Test retrieving the value from session
        response = client.get('/get')
        assert response.data == b'test_value'

        # Test clearing the session
        with flask.session_transaction() as session:
            session.clear()
        
        # Test default value again after clearing session
        response = client.get('/get')
        assert response.data == b'None'
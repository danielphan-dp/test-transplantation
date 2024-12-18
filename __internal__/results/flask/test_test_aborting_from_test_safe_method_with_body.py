import flask
import pytest

def test_get_value_from_session(app):
    with app.test_client() as c:
        # Test default value when session is empty
        rv = c.get('/get')
        assert rv.data == b'None'

        # Test setting a value in the session
        with flask.session_transaction() as session:
            session['value'] = 'Test Value'
        
        # Test retrieving the value from session
        rv = c.get('/get')
        assert rv.data == b'Test Value'

def test_get_value_with_no_session(app):
    with app.test_client() as c:
        # Ensure session is empty
        flask.session.clear()
        rv = c.get('/get')
        assert rv.data == b'None'
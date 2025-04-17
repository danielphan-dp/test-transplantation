import pytest
import flask

def test_get_session_value(app, client):
    """Test the /get endpoint to ensure it returns the correct session value."""
    
    @app.route('/set/<value>')
    def set_value(value):
        flask.session['value'] = value
        return 'Value set'

    # Test default session value
    response = client.get('/get')
    assert response.data == b'None'

    # Test setting and getting a session value
    client.get('/set/test_value')
    response = client.get('/get')
    assert response.data == b'test_value'

def test_get_session_value_empty(app, client):
    """Test the /get endpoint when session value is not set."""
    
    response = client.get('/get')
    assert response.data == b'None'

def test_get_session_value_none(app, client):
    """Test the /get endpoint when session value is explicitly set to None."""
    
    @app.route('/set_none')
    def set_none():
        flask.session['value'] = None
        return 'Value set to None'

    client.get('/set_none')
    response = client.get('/get')
    assert response.data == b'None'
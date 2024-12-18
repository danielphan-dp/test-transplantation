import pytest
import flask

def test_get_value_from_session(app, client):
    """Test retrieving value from session."""
    
    @app.route('/set/<value>')
    def set_value(value):
        flask.session['value'] = value
        return 'Value set'

    @app.route('/get')
    def get_value():
        return flask.session.get('value', 'None')

    client.get('/set/test_value')
    response = client.get('/get')
    assert response.data == b'test_value'

def test_get_value_default(app, client):
    """Test retrieving default value when session is empty."""
    
    response = client.get('/get')
    assert response.data == b'None'

def test_get_value_after_clear(app, client):
    """Test retrieving value after clearing session."""
    
    @app.route('/set/<value>')
    def set_value(value):
        flask.session['value'] = value
        return 'Value set'

    @app.route('/clear')
    def clear_session():
        flask.session.clear()
        return 'Session cleared'

    client.get('/set/test_value')
    client.get('/clear')
    response = client.get('/get')
    assert response.data == b'None'
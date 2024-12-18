import pytest
import flask

def test_get_session_value(app, client):
    """Test the /get route to ensure it returns the correct session value."""
    
    @app.route('/set/<value>')
    def set_value(value):
        flask.session['value'] = value
        return 'Value set'

    # Test default session value
    response = client.get('/get')
    assert response.data == b'None'

    # Test setting a session value
    client.get('/set/test_value')
    response = client.get('/get')
    assert response.data == b'test_value'

    # Test setting another session value
    client.get('/set/another_value')
    response = client.get('/get')
    assert response.data == b'another_value'

    # Test clearing the session
    with client.session_transaction() as sess:
        sess.clear()
    response = client.get('/get')
    assert response.data == b'None'
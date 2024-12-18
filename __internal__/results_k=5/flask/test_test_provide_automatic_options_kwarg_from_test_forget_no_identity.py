import flask
import pytest

def test_get_session_value(app, client):
    @app.route('/set', methods=['POST'])
    def set_value():
        flask.session['value'] = 'test_value'
        return '', 204

    @app.route('/get')
    def get():
        v = flask.session.get('value', 'None')
        return v

    # Test default session value
    response = client.get('/get')
    assert response.data == b'None'

    # Set session value
    client.post('/set')
    
    # Test session value after setting it
    response = client.get('/get')
    assert response.data == b'test_value'

def test_get_session_value_with_no_session(app, client):
    @app.route('/get')
    def get():
        v = flask.session.get('value', 'None')
        return v

    # Test session value when no session exists
    response = client.get('/get')
    assert response.data == b'None'
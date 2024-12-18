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
    
    # Test session value after setting
    response = client.get('/get')
    assert response.data == b'test_value'

    # Test session value after clearing
    with client.session_transaction() as session:
        session.clear()
    response = client.get('/get')
    assert response.data == b'None'

    # Test session value with a different key
    @app.route('/set_another', methods=['POST'])
    def set_another_value():
        flask.session['another_value'] = 'another_test_value'
        return '', 204

    client.post('/set_another')
    response = client.get('/get')
    assert response.data == b'None'  # Ensure it does not return the other key's value

    # Test session value with a non-existent key
    response = client.get('/get_non_existent')
    assert response.data == b'None'  # Ensure it returns default for non-existent key
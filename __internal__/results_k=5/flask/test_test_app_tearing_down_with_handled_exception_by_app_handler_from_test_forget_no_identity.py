import pytest
import flask

def test_get_session_value_none(app, client):
    with app.app_context():
        response = client.get('/get')
        assert response.data == b'None'

def test_get_session_value_set(app, client):
    with app.app_context():
        flask.session['value'] = 'test_value'
        response = client.get('/get')
        assert response.data == b'test_value'

def test_get_session_value_empty_string(app, client):
    with app.app_context():
        flask.session['value'] = ''
        response = client.get('/get')
        assert response.data == b''

def test_get_session_value_nonexistent_key(app, client):
    with app.app_context():
        response = client.get('/get')
        assert response.data == b'None'  # Default value when key does not exist

def test_get_session_value_after_clear(app, client):
    with app.app_context():
        flask.session['value'] = 'test_value'
        flask.session.clear()
        response = client.get('/get')
        assert response.data == b'None'  # Should return default after clear

def test_get_session_value_with_teardown(app, client):
    cleanup_stuff = []

    @app.teardown_appcontext
    def cleanup(exception):
        cleanup_stuff.append(exception)

    with app.app_context():
        flask.session['value'] = 'test_value'
        response = client.get('/get')
        assert response.data == b'test_value'
    
    assert cleanup_stuff == [None]  # Ensure cleanup is called without exceptions
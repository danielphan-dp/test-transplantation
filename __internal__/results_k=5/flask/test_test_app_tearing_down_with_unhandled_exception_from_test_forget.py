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
        assert response.data == b'None'  # Testing default value when key does not exist

def test_get_session_value_after_teardown(app, client):
    cleanup_stuff = []

    @app.teardown_appcontext
    def cleanup(exception):
        cleanup_stuff.append(exception)

    with app.app_context():
        flask.session['value'] = 'test_value'
        response = client.get('/get')
        assert response.data == b'test_value'

    assert len(cleanup_stuff) == 0  # Ensure no exception during teardown
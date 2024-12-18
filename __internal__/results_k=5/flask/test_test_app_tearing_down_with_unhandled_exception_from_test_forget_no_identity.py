import pytest
import flask

@pytest.fixture
def client(app):
    return app.test_client()

def test_get_session_value_none(client, app):
    with app.app_context():
        response = client.get('/get')
        assert response.data == b'None'

def test_get_session_value_set(client, app):
    with app.app_context():
        flask.session['value'] = 'test_value'
        response = client.get('/get')
        assert response.data == b'test_value'

def test_get_session_value_empty_string(client, app):
    with app.app_context():
        flask.session['value'] = ''
        response = client.get('/get')
        assert response.data == b''

def test_get_session_value_nonexistent_key(client, app):
    with app.app_context():
        response = client.get('/get')
        assert response.data == b'None'  # Default value when key does not exist

def test_get_session_value_after_teardown(client, app):
    cleanup_stuff = []

    @app.teardown_appcontext
    def cleanup(exception):
        cleanup_stuff.append(exception)

    with app.app_context():
        flask.session['value'] = 'test_value'
        response = client.get('/get')
        assert response.data == b'test_value'

    assert len(cleanup_stuff) == 0  # No exception should be raised during normal operation
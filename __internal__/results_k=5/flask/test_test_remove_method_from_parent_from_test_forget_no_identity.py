import flask
import pytest

@pytest.fixture
def client(app):
    return app.test_client()

def test_get_method_with_session_value(client, app):
    with app.app_context():
        flask.session['value'] = 'Test Value'
        response = client.get('/get')
        assert response.data == b'Test Value'

def test_get_method_with_no_session_value(client, app):
    with app.app_context():
        response = client.get('/get')
        assert response.data == b'None'

def test_get_method_with_empty_session_value(client, app):
    with app.app_context():
        flask.session['value'] = ''
        response = client.get('/get')
        assert response.data == b''

def test_get_method_with_none_session_value(client, app):
    with app.app_context():
        flask.session['value'] = None
        response = client.get('/get')
        assert response.data == b'None'
import pytest
import flask

@pytest.fixture
def client(app):
    return app.test_client()

def test_get_method_with_session_value(client, app):
    with app.app_context():
        flask.session['value'] = 'TestValue'
        response = client.get('/get')
        assert response.data == b'TestValue'

def test_get_method_with_none_value(client, app):
    with app.app_context():
        flask.session.pop('value', None)
        response = client.get('/get')
        assert response.data == b'None'

def test_get_method_with_empty_string(client, app):
    with app.app_context():
        flask.session['value'] = ''
        response = client.get('/get')
        assert response.data == b''

def test_get_method_with_special_characters(client, app):
    with app.app_context():
        flask.session['value'] = 'Special@#$%'
        response = client.get('/get')
        assert response.data == b'Special@#$%'
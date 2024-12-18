import flask
import pytest

@pytest.fixture
def client(app):
    return app.test_client()

def test_get_with_default_value(client):
    response = client.get('/get')
    assert response.data == b'None'

def test_get_with_set_value(client, app):
    with app.app_context():
        flask.session['value'] = 'Test Value'
    response = client.get('/get')
    assert response.data == b'Test Value'

def test_get_with_empty_value(client, app):
    with app.app_context():
        flask.session['value'] = ''
    response = client.get('/get')
    assert response.data == b''

def test_get_with_none_value(client, app):
    with app.app_context():
        flask.session['value'] = None
    response = client.get('/get')
    assert response.data == b'None'
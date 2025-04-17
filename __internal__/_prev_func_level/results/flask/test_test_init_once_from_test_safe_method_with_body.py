import flask
import pytest

@pytest.fixture
def client(app):
    return app.test_client()

def test_get_value_none(client):
    response = client.get('/get')
    assert response.data == b'None'

def test_get_value_set(client, app):
    with app.app_context():
        flask.session['value'] = 'Test Value'
    response = client.get('/get')
    assert response.data == b'Test Value'

def test_get_value_empty_string(client, app):
    with app.app_context():
        flask.session['value'] = ''
    response = client.get('/get')
    assert response.data == b''

def test_get_value_nonexistent(client):
    response = client.get('/get')
    assert response.data == b'None'
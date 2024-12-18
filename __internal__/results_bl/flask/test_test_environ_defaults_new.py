import pytest
import flask

@pytest.fixture
def client(app):
    return app.test_client()

def test_get_value_none(client):
    with client:
        rv = client.get('/get')
        assert rv.data == b'None'

def test_get_value_set(client, app):
    with app.app_context():
        flask.session['value'] = 'test_value'
        rv = client.get('/get')
        assert rv.data == b'test_value'

def test_get_value_empty_string(client, app):
    with app.app_context():
        flask.session['value'] = ''
        rv = client.get('/get')
        assert rv.data == b''

def test_get_value_nonexistent_key(client, app):
    with app.app_context():
        rv = client.get('/get')
        assert rv.data == b'None'
import flask
import pytest

@pytest.fixture
def client(app):
    return app.test_client()

def test_get_with_default_value(client):
    rv = client.get('/get')
    assert rv.data == b'None'

def test_get_with_set_value(client, app):
    with app.app_context():
        flask.session['value'] = 'Test Value'
    rv = client.get('/get')
    assert rv.data == b'Test Value'

def test_get_with_empty_value(client, app):
    with app.app_context():
        flask.session['value'] = ''
    rv = client.get('/get')
    assert rv.data == b''

def test_get_with_none_value(client, app):
    with app.app_context():
        flask.session['value'] = None
    rv = client.get('/get')
    assert rv.data == b'None'
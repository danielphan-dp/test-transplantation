import flask
import pytest

@pytest.fixture
def app():
    app = flask.Flask(__name__)
    app.secret_key = 'test_secret'
    return app

def test_get_value_none(app):
    client = app.test_client()
    rv = client.get('/get')
    assert rv.data == b'None'

def test_get_value_set(app):
    with app.test_request_context():
        flask.session['value'] = 'test_value'
    client = app.test_client()
    rv = client.get('/get')
    assert rv.data == b'test_value'

def test_get_value_empty_string(app):
    with app.test_request_context():
        flask.session['value'] = ''
    client = app.test_client()
    rv = client.get('/get')
    assert rv.data == b''

def test_get_value_nonexistent_key(app):
    with app.test_request_context():
        flask.session.clear()
    client = app.test_client()
    rv = client.get('/get')
    assert rv.data == b'None'
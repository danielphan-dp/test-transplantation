import flask
import pytest

@pytest.fixture
def session_app():
    app = flask.Flask(__name__)
    app.secret_key = 'test_secret'
    with app.test_request_context():
        yield app

@app.route('/get')
def get():
    v = flask.session.get('value', 'None')
    return v

def test_get_value_none(session_app):
    client = session_app.test_client()
    response = client.get('/get')
    assert response.data == b'None'

def test_get_value_set(session_app):
    with session_app.test_request_context():
        flask.session['value'] = 'test_value'
    client = session_app.test_client()
    response = client.get('/get')
    assert response.data == b'test_value'

def test_get_value_empty_string(session_app):
    with session_app.test_request_context():
        flask.session['value'] = ''
    client = session_app.test_client()
    response = client.get('/get')
    assert response.data == b''

def test_get_value_none_after_clear(session_app):
    with session_app.test_request_context():
        flask.session['value'] = 'test_value'
        flask.session.clear()
    client = session_app.test_client()
    response = client.get('/get')
    assert response.data == b'None'
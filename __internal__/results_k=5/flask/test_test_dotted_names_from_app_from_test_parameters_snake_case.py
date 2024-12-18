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
    client = session_app.test_client()
    with client.session_transaction() as session:
        session['value'] = 'test_value'
    response = client.get('/get')
    assert response.data == b'test_value'

def test_get_value_empty(session_app):
    client = session_app.test_client()
    with client.session_transaction() as session:
        session['value'] = ''
    response = client.get('/get')
    assert response.data == b''

def test_get_value_none_after_clear(session_app):
    client = session_app.test_client()
    with client.session_transaction() as session:
        session['value'] = 'test_value'
    with client.session_transaction() as session:
        session.clear()
    response = client.get('/get')
    assert response.data == b'None'
import flask
import pytest

def test_get_session_value_none():
    app = flask.Flask(__name__)
    app.secret_key = 'test_secret'
    client = app.test_client()

    @app.route('/get')
    def get():
        v = flask.session.get('value', 'None')
        return v

    response = client.get('/get')
    assert response.data == b'None'

def test_get_session_value_set():
    app = flask.Flask(__name__)
    app.secret_key = 'test_secret'
    client = app.test_client()

    with client.session_transaction() as session:
        session['value'] = 'test_value'

    @app.route('/get')
    def get():
        v = flask.session.get('value', 'None')
        return v

    response = client.get('/get')
    assert response.data == b'test_value'

def test_get_session_value_empty_string():
    app = flask.Flask(__name__)
    app.secret_key = 'test_secret'
    client = app.test_client()

    with client.session_transaction() as session:
        session['value'] = ''

    @app.route('/get')
    def get():
        v = flask.session.get('value', 'None')
        return v

    response = client.get('/get')
    assert response.data == b''

def test_get_session_value_none_with_default():
    app = flask.Flask(__name__)
    app.secret_key = 'test_secret'
    client = app.test_client()

    @app.route('/get')
    def get():
        v = flask.session.get('value', 'default_value')
        return v

    response = client.get('/get')
    assert response.data == b'default_value'
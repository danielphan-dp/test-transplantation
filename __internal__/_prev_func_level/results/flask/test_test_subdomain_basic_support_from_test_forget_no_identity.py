import flask
import pytest

def test_get_session_value_none():
    app = flask.Flask(__name__)
    client = app.test_client()

    @app.route('/get')
    def get():
        v = flask.session.get('value', 'None')
        return v

    with app.test_request_context():
        response = client.get('/get')
        assert response.data == b'None'

def test_get_session_value_set():
    app = flask.Flask(__name__)
    app.secret_key = 'test_secret'
    client = app.test_client()

    @app.route('/get')
    def get():
        v = flask.session.get('value', 'None')
        return v

    with app.test_request_context():
        flask.session['value'] = 'test_value'
        response = client.get('/get')
        assert response.data == b'test_value'

def test_get_session_value_empty_string():
    app = flask.Flask(__name__)
    app.secret_key = 'test_secret'
    client = app.test_client()

    @app.route('/get')
    def get():
        v = flask.session.get('value', 'None')
        return v

    with app.test_request_context():
        flask.session['value'] = ''
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

    with app.test_request_context():
        response = client.get('/get')
        assert response.data == b'default_value'
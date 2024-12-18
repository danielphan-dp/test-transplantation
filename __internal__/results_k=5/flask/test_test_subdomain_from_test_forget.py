import flask
import pytest

def test_get_value_none():
    app = flask.Flask(__name__)
    client = app.test_client()

    @app.route('/get')
    def get():
        v = flask.session.get('value', 'None')
        return v

    with app.test_request_context():
        response = client.get('/get')
        assert response.data == b'None'
        assert response.status_code == 200

def test_get_value_set():
    app = flask.Flask(__name__)
    app.secret_key = 'test_secret'
    client = app.test_client()

    @app.route('/set_value/<value>')
    def set_value(value):
        flask.session['value'] = value
        return 'Value set'

    @app.route('/get')
    def get():
        v = flask.session.get('value', 'None')
        return v

    with app.test_request_context():
        client.get('/set_value/test_value')
        response = client.get('/get')
        assert response.data == b'test_value'
        assert response.status_code == 200

def test_get_value_empty():
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
        assert response.status_code == 200

def test_get_value_none_with_different_key():
    app = flask.Flask(__name__)
    app.secret_key = 'test_secret'
    client = app.test_client()

    @app.route('/get')
    def get():
        v = flask.session.get('value', 'None')
        return v

    with app.test_request_context():
        flask.session['other_key'] = 'some_value'
        response = client.get('/get')
        assert response.data == b'None'
        assert response.status_code == 200
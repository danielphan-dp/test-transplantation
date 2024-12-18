import flask
from flask.globals import request_ctx
from flask.sessions import SessionInterface
import pytest

def test_get_with_default_value():
    app = flask.Flask(__name__)

    @app.route('/get')
    def get():
        v = flask.session.get('value', 'None')
        return v

    with app.test_client() as client:
        response = client.get('/get')
        assert response.data.decode() == 'None'
        assert response.status_code == 200

def test_get_with_set_value():
    app = flask.Flask(__name__)
    app.secret_key = 'test_secret'

    @app.route('/set_value/<value>')
    def set_value(value):
        flask.session['value'] = value
        return 'Value set'

    @app.route('/get')
    def get():
        v = flask.session.get('value', 'None')
        return v

    with app.test_client() as client:
        client.get('/set_value/test_value')
        response = client.get('/get')
        assert response.data.decode() == 'test_value'
        assert response.status_code == 200

def test_get_with_no_session():
    app = flask.Flask(__name__)

    @app.route('/get')
    def get():
        v = flask.session.get('value', 'None')
        return v

    with app.test_client() as client:
        response = client.get('/get')
        assert response.data.decode() == 'None'
        assert response.status_code == 200

def test_get_with_empty_session():
    app = flask.Flask(__name__)
    app.secret_key = 'test_secret'

    @app.route('/get')
    def get():
        v = flask.session.get('value', 'None')
        return v

    with app.test_client() as client:
        client.set_cookie('localhost', 'session', '')
        response = client.get('/get')
        assert response.data.decode() == 'None'
        assert response.status_code == 200

def test_get_with_invalid_session():
    app = flask.Flask(__name__)
    app.secret_key = 'test_secret'

    @app.route('/get')
    def get():
        v = flask.session.get('value', 'None')
        return v

    with app.test_client() as client:
        client.set_cookie('localhost', 'session', 'invalid_session_data')
        response = client.get('/get')
        assert response.data.decode() == 'None'
        assert response.status_code == 200
import flask
import pytest

def test_get_value_none():
    app = flask.Flask(__name__)
    app.secret_key = 'test_secret'
    client = app.test_client()

    @app.route('/get')
    def get():
        v = flask.session.get('value', 'None')
        return v

    with client:
        response = client.get('/get')
        assert response.status_code == 200
        assert response.data == b'None'

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

    with client:
        client.get('/set_value/test_value')
        response = client.get('/get')
        assert response.status_code == 200
        assert response.data == b'test_value'

def test_get_value_empty():
    app = flask.Flask(__name__)
    app.secret_key = 'test_secret'
    client = app.test_client()

    @app.route('/get')
    def get():
        v = flask.session.get('value', 'None')
        return v

    with client:
        response = client.get('/get')
        assert response.status_code == 200
        assert response.data == b'None'
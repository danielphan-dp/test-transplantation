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

    @app.route('/get')
    def get():
        v = flask.session.get('value', 'None')
        return v

    with app.test_request_context():
        with flask.session_transaction() as session:
            session['value'] = 'test_value'
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
        with flask.session_transaction() as session:
            session['value'] = ''
        response = client.get('/get')
        assert response.data == b''
        assert response.status_code == 200

def test_get_value_nonexistent():
    app = flask.Flask(__name__)
    app.secret_key = 'test_secret'
    client = app.test_client()

    @app.route('/get')
    def get():
        v = flask.session.get('value', 'None')
        return v

    with app.test_request_context():
        response = client.get('/get')
        assert response.data == b'None'
        assert response.status_code == 200
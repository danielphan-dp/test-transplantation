import flask
import pytest
from werkzeug.exceptions import HTTPException, NotFound, Forbidden

def test_get_method_with_session_value():
    app = flask.Flask(__name__)
    app.secret_key = 'test_secret'

    @app.route('/get')
    def get():
        v = flask.session.get('value', 'None')
        return v

    client = app.test_client()

    with app.test_request_context():
        flask.session['value'] = 'test_value'
        response = client.get('/get')
        assert response.data == b'test_value'

def test_get_method_without_session_value():
    app = flask.Flask(__name__)
    app.secret_key = 'test_secret'

    @app.route('/get')
    def get():
        v = flask.session.get('value', 'None')
        return v

    client = app.test_client()

    with app.test_request_context():
        response = client.get('/get')
        assert response.data == b'None'

def test_get_method_with_invalid_session():
    app = flask.Flask(__name__)
    app.secret_key = 'test_secret'

    @app.route('/get')
    def get():
        v = flask.session.get('value', 'None')
        return v

    client = app.test_client()

    with app.test_request_context():
        flask.session['value'] = None
        response = client.get('/get')
        assert response.data == b'None'
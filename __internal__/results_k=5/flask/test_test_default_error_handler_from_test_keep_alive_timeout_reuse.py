import flask
import pytest
from werkzeug.exceptions import HTTPException, NotFound, Forbidden

def test_get_method_with_default_value():
    app = flask.Flask(__name__)
    app.secret_key = 'test_secret'

    @app.route('/get')
    def get():
        v = flask.session.get('value', 'None')
        return v

    client = app.test_client()
    response = client.get('/get')
    assert response.data == b'None'

def test_get_method_with_set_value():
    app = flask.Flask(__name__)
    app.secret_key = 'test_secret'

    @app.route('/get')
    def get():
        v = flask.session.get('value', 'None')
        return v

    with app.test_request_context():
        flask.session['value'] = 'test_value'
        client = app.test_client()
        response = client.get('/get')
        assert response.data == b'test_value'

def test_get_method_with_empty_session():
    app = flask.Flask(__name__)
    app.secret_key = 'test_secret'

    @app.route('/get')
    def get():
        v = flask.session.get('value', 'None')
        return v

    client = app.test_client()
    response = client.get('/get')
    assert response.data == b'None'

def test_get_method_with_none_value():
    app = flask.Flask(__name__)
    app.secret_key = 'test_secret'

    @app.route('/get')
    def get():
        v = flask.session.get('value', None)
        return str(v)

    client = app.test_client()
    response = client.get('/get')
    assert response.data == b'None'
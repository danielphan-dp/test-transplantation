import pytest
import flask
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

    @app.route('/set_value/<value>')
    def set_value(value):
        flask.session['value'] = value
        return 'Value set'

    @app.route('/get')
    def get():
        v = flask.session.get('value', 'None')
        return v

    client = app.test_client()
    client.get('/set_value/test_value')
    response = client.get('/get')
    assert response.data == b'test_value'

def test_get_method_with_no_session():
    app = flask.Flask(__name__)
    app.secret_key = 'test_secret'

    @app.route('/get')
    def get():
        v = flask.session.get('value', 'None')
        return v

    client = app.test_client()
    response = client.get('/get')
    assert response.data == b'None'

def test_get_method_with_empty_session():
    app = flask.Flask(__name__)
    app.secret_key = 'test_secret'

    @app.route('/get')
    def get():
        v = flask.session.get('value', 'None')
        return v

    client = app.test_client()
    with client.session_transaction() as sess:
        sess.clear()
    response = client.get('/get')
    assert response.data == b'None'
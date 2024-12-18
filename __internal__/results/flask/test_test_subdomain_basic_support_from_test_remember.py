import flask
import pytest

def test_get_value_from_session():
    app = flask.Flask(__name__)
    app.secret_key = 'test_secret'
    client = app.test_client()

    @app.route('/set/<value>')
    def set_value(value):
        flask.session['value'] = value
        return 'Value set'

    @app.route('/get')
    def get():
        v = flask.session.get('value', 'None')
        return v

    # Test setting a value in the session
    client.get('/set/test_value')
    rv = client.get('/get')
    assert rv.data == b'test_value'

def test_get_value_not_set():
    app = flask.Flask(__name__)
    app.secret_key = 'test_secret'
    client = app.test_client()

    @app.route('/get')
    def get():
        v = flask.session.get('value', 'None')
        return v

    # Test getting a value when none is set
    rv = client.get('/get')
    assert rv.data == b'None'

def test_get_value_with_default():
    app = flask.Flask(__name__)
    app.secret_key = 'test_secret'
    client = app.test_client()

    @app.route('/get')
    def get():
        v = flask.session.get('value', 'default_value')
        return v

    # Test getting a value with a default when none is set
    rv = client.get('/get')
    assert rv.data == b'default_value'
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

    with client.session_transaction() as session:
        session['value'] = None

    rv = client.get('/get')
    assert rv.data == b'None'

def test_get_session_value_set():
    app = flask.Flask(__name__)
    app.secret_key = 'test_secret'
    client = app.test_client()

    @app.route('/get')
    def get():
        v = flask.session.get('value', 'None')
        return v

    with client.session_transaction() as session:
        session['value'] = 'test_value'

    rv = client.get('/get')
    assert rv.data == b'test_value'

def test_get_session_value_default():
    app = flask.Flask(__name__)
    app.secret_key = 'test_secret'
    client = app.test_client()

    @app.route('/get')
    def get():
        v = flask.session.get('value', 'None')
        return v

    rv = client.get('/get')
    assert rv.data == b'None'
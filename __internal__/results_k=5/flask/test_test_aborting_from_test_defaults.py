import flask
import pytest

@pytest.fixture
def app():
    app = flask.Flask(__name__)
    app.secret_key = 'test_secret'
    return app

def test_get_value_none(app):
    with app.test_client() as c:
        rv = c.get('/get')
        assert rv.data == b'None'

def test_get_value_set(app):
    with app.test_client() as c:
        with flask.session_transaction() as session:
            session['value'] = 'test_value'
        rv = c.get('/get')
        assert rv.data == b'test_value'

def test_get_value_empty_string(app):
    with app.test_client() as c:
        with flask.session_transaction() as session:
            session['value'] = ''
        rv = c.get('/get')
        assert rv.data == b''

def test_get_value_none_after_clear(app):
    with app.test_client() as c:
        with flask.session_transaction() as session:
            session['value'] = 'test_value'
        with flask.session_transaction() as session:
            session.clear()
        rv = c.get('/get')
        assert rv.data == b'None'
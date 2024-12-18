import flask
import pytest

@pytest.fixture
def app():
    app = flask.Flask(__name__)
    app.secret_key = 'test_secret'
    return app

def test_get_value_from_session(app):
    client = app.test_client()
    with app.app_context():
        flask.session['value'] = 'test_value'
        rv = client.get('/get')
        assert rv.data == b'test_value'

def test_get_value_not_set(app):
    client = app.test_client()
    with app.app_context():
        rv = client.get('/get')
        assert rv.data == b'None'

def test_get_value_after_clear_session(app):
    client = app.test_client()
    with app.app_context():
        flask.session['value'] = 'test_value'
        flask.session.clear()
        rv = client.get('/get')
        assert rv.data == b'None'

def test_get_value_with_different_session(app):
    client = app.test_client()
    with app.app_context():
        flask.session['value'] = 'first_value'
        rv = client.get('/get')
        assert rv.data == b'first_value'
        flask.session['value'] = 'second_value'
        rv = client.get('/get')
        assert rv.data == b'second_value'
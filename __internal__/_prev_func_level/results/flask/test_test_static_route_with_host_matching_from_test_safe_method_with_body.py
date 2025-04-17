import flask
import pytest

@pytest.fixture
def app():
    app = flask.Flask(__name__)
    app.secret_key = 'test_secret'
    return app

def test_get_value_from_session(app):
    with app.test_client() as client:
        with app.app_context():
            flask.session['value'] = 'test_value'
        response = client.get('/get')
        assert response.data.decode() == 'test_value'

def test_get_value_not_set(app):
    with app.test_client() as client:
        response = client.get('/get')
        assert response.data.decode() == 'None'

def test_get_value_with_none(app):
    with app.test_client() as client:
        with app.app_context():
            flask.session['value'] = None
        response = client.get('/get')
        assert response.data.decode() == 'None'

def test_get_value_with_empty_string(app):
    with app.test_client() as client:
        with app.app_context():
            flask.session['value'] = ''
        response = client.get('/get')
        assert response.data.decode() == ''
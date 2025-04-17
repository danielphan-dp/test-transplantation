import flask
import pytest

@pytest.fixture
def app():
    app = flask.Flask(__name__)
    app.secret_key = 'test_secret'
    return app

def test_get_value_from_session(app):
    with app.test_client() as client:
        with flask.session_transaction() as session:
            session['value'] = 'Test Value'
        response = client.get('/get')
        assert response.data == b'Test Value'

def test_get_value_not_set(app):
    with app.test_client() as client:
        response = client.get('/get')
        assert response.data == b'None'

def test_get_value_with_none(app):
    with app.test_client() as client:
        with flask.session_transaction() as session:
            session['value'] = None
        response = client.get('/get')
        assert response.data == b'None'
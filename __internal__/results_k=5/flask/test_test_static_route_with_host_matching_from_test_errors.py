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
        assert response.status_code == 200

def test_get_value_not_set(app):
    with app.test_client() as client:
        response = client.get('/get')
        assert response.data.decode() == 'None'
        assert response.status_code == 200

def test_get_value_with_different_session_value(app):
    with app.test_client() as client:
        with app.app_context():
            flask.session['value'] = 'another_value'
        response = client.get('/get')
        assert response.data.decode() == 'another_value'
        assert response.status_code == 200

def test_get_value_after_session_clear(app):
    with app.test_client() as client:
        with app.app_context():
            flask.session['value'] = 'value_to_clear'
            flask.session.clear()
        response = client.get('/get')
        assert response.data.decode() == 'None'
        assert response.status_code == 200

def test_get_value_with_no_session(app):
    with app.test_client() as client:
        response = client.get('/get')
        assert response.data.decode() == 'None'
        assert response.status_code == 200
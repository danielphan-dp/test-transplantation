import flask
import pytest

def test_get_value_from_session():
    app = flask.Flask(__name__)
    app.secret_key = 'test_secret'
    with app.test_client() as client:
        with app.app_context():
            flask.session['value'] = 'test_value'
            response = client.get('/get')
            assert response.data.decode() == 'test_value'

def test_get_value_not_set_in_session():
    app = flask.Flask(__name__)
    app.secret_key = 'test_secret'
    with app.test_client() as client:
        response = client.get('/get')
        assert response.data.decode() == 'None'

def test_get_value_after_session_clear():
    app = flask.Flask(__name__)
    app.secret_key = 'test_secret'
    with app.test_client() as client:
        with app.app_context():
            flask.session['value'] = 'test_value'
            flask.session.clear()
            response = client.get('/get')
            assert response.data.decode() == 'None'
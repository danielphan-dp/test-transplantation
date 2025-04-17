import flask
import pytest
from flask import Flask

@pytest.fixture
def app():
    app = Flask(__name__)
    app.secret_key = 'test_secret'
    return app

def test_get_value_from_session(app):
    with app.test_client() as client:
        with flask.session_transaction() as session:
            session['value'] = 'test_value'
        response = client.get('/get')
        assert response.data.decode() == 'test_value'

def test_get_value_not_set(app):
    with app.test_client() as client:
        response = client.get('/get')
        assert response.data.decode() == 'None'

def test_get_value_after_clearing_session(app):
    with app.test_client() as client:
        with flask.session_transaction() as session:
            session['value'] = 'test_value'
        with flask.session_transaction() as session:
            session.clear()
        response = client.get('/get')
        assert response.data.decode() == 'None'
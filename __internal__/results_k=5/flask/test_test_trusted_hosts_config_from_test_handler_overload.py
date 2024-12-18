import flask
import pytest
from flask import Flask

@pytest.fixture
def app():
    app = Flask(__name__)
    app.secret_key = 'test_secret'
    return app

def test_get_session_value(app):
    with app.test_client() as client:
        with flask.session_transaction() as session:
            session['value'] = 'test_value'
        response = client.get('/get')
        assert response.data.decode() == 'test_value'

def test_get_session_value_default(app):
    with app.test_client() as client:
        response = client.get('/get')
        assert response.data.decode() == 'None'

def test_get_session_value_empty(app):
    with app.test_client() as client:
        with flask.session_transaction() as session:
            session['value'] = ''
        response = client.get('/get')
        assert response.data.decode() == ''
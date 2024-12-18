import flask
import pytest
from flask import Flask

@pytest.fixture
def app():
    app = Flask(__name__)
    app.secret_key = 'test_secret'
    return app

def test_get_session_value_none(app):
    with app.test_client() as client:
        response = client.get('/get')
        assert response.data == b'None'

def test_get_session_value_set(app):
    with app.test_client() as client:
        with client.session_transaction() as session:
            session['value'] = 'test_value'
        response = client.get('/get')
        assert response.data == b'test_value'

def test_get_session_value_empty(app):
    with app.test_client() as client:
        with client.session_transaction() as session:
            session['value'] = ''
        response = client.get('/get')
        assert response.data == b''

def test_get_session_value_nonexistent(app):
    with app.test_client() as client:
        response = client.get('/get')
        assert response.data == b'None'
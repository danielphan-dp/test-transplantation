import pytest
from flask import Flask, session

@pytest.fixture
def app():
    app = Flask(__name__)
    app.secret_key = 'test_secret'
    return app

def test_get_value_from_session(app):
    with app.test_client() as client:
        with client.session_transaction() as sess:
            sess['value'] = 'test_value'
        response = client.get('/get')
        assert response.data == b'test_value'

def test_get_value_not_set(app):
    with app.test_client() as client:
        response = client.get('/get')
        assert response.data == b'None'

def test_get_value_empty_string(app):
    with app.test_client() as client:
        with client.session_transaction() as sess:
            sess['value'] = ''
        response = client.get('/get')
        assert response.data == b''

def test_get_value_none(app):
    with app.test_client() as client:
        with client.session_transaction() as sess:
            sess['value'] = None
        response = client.get('/get')
        assert response.data == b'None'
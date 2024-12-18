import pytest
from flask import Flask, session

@pytest.fixture
def app():
    app = Flask(__name__)
    app.secret_key = 'test_secret'
    return app

def test_get_value_none(app, client):
    with app.test_request_context():
        session['value'] = None
        response = client.get('/get')
        assert response.data == b'None'

def test_get_value_set(app, client):
    with app.test_request_context():
        session['value'] = 'test_value'
        response = client.get('/get')
        assert response.data == b'test_value'

def test_get_value_empty_string(app, client):
    with app.test_request_context():
        session['value'] = ''
        response = client.get('/get')
        assert response.data == b''

def test_get_value_nonexistent(app, client):
    with app.test_request_context():
        response = client.get('/get')
        assert response.data == b'None'
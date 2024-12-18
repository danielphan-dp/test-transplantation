import pytest
import flask
from flask import Flask, session

@pytest.fixture
def app():
    app = Flask(__name__)
    app.secret_key = 'test_secret'
    return app

@pytest.fixture
def client(app):
    return app.test_client()

def test_get_session_value_none(client):
    response = client.get('/get')
    assert response.status_code == 200
    assert response.data == b'None'

def test_get_session_value_set(client):
    with client.session_transaction() as sess:
        sess['value'] = 'test_value'
    response = client.get('/get')
    assert response.status_code == 200
    assert response.data == b'test_value'

def test_get_session_value_empty(client):
    with client.session_transaction() as sess:
        sess['value'] = ''
    response = client.get('/get')
    assert response.status_code == 200
    assert response.data == b''

def test_get_session_value_nonexistent(client):
    response = client.get('/get')
    assert response.status_code == 200
    assert response.data == b'None'
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
    assert response.data == b'None'

def test_get_session_value_set(client):
    with client.session_transaction() as sess:
        sess['value'] = 'test_value'
    response = client.get('/get')
    assert response.data == b'test_value'

def test_get_session_value_empty(client):
    with client.session_transaction() as sess:
        sess['value'] = ''
    response = client.get('/get')
    assert response.data == b''

def test_get_session_value_after_teardown(client):
    with client.session_transaction() as sess:
        sess['value'] = 'value_before_teardown'
    response = client.get('/get')
    assert response.data == b'value_before_teardown'
    
    with client.session_transaction() as sess:
        sess.clear()
    response_after_teardown = client.get('/get')
    assert response_after_teardown.data == b'None'
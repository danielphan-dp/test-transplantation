import pytest
from flask import Flask, session

@pytest.fixture
def app():
    app = Flask(__name__)
    app.secret_key = 'test_secret'
    return app

@pytest.fixture
def client(app):
    return app.test_client()

@app.route('/get')
def get():
    v = session.get('value', 'None')
    return v

def test_get_no_value(client):
    response = client.get('/get')
    assert response.data == b'None'

def test_get_with_value(client):
    with client.session_transaction() as sess:
        sess['value'] = 'test_value'
    response = client.get('/get')
    assert response.data == b'test_value'

def test_get_with_none_value(client):
    with client.session_transaction() as sess:
        sess['value'] = None
    response = client.get('/get')
    assert response.data == b'None'
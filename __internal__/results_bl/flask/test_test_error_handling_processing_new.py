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

def test_get_value_none(client):
    resp = client.get('/get')
    assert resp.data.decode() == 'None'

def test_get_value_set(client):
    with client.session_transaction() as sess:
        sess['value'] = 'test_value'
    resp = client.get('/get')
    assert resp.data.decode() == 'test_value'

def test_get_value_empty(client):
    with client.session_transaction() as sess:
        sess['value'] = ''
    resp = client.get('/get')
    assert resp.data.decode() == ''
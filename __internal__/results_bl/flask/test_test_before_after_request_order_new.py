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

@app.route('/set/<value>')
def set_value(value):
    session['value'] = value
    return 'Value set'

def test_get_value_none(client):
    rv = client.get('/get')
    assert rv.data == b'None'

def test_get_value_set(client):
    client.get('/set/test_value')
    rv = client.get('/get')
    assert rv.data == b'test_value'

def test_get_value_empty_string(client):
    client.get('/set/')
    rv = client.get('/get')
    assert rv.data == b''
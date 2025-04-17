import pytest
from flask import Flask, session

@pytest.fixture
def app():
    app = Flask(__name__)
    app.secret_key = 'test_secret'
    return app

@app.route('/set/<value>')
def set_value(value):
    session['value'] = value
    return "Value set"

def test_get_value_none(app):
    with app.test_client() as client:
        response = client.get('/get')
        assert response.data == b'None'

def test_get_value_set(app):
    with app.test_client() as client:
        client.get('/set/test_value')
        response = client.get('/get')
        assert response.data == b'test_value'

def test_get_value_empty_string(app):
    with app.test_client() as client:
        client.get('/set/')
        response = client.get('/get')
        assert response.data == b''

def test_get_value_after_clear(app):
    with app.test_client() as client:
        client.get('/set/test_value')
        session.clear()
        response = client.get('/get')
        assert response.data == b'None'
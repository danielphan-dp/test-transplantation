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

def test_get_value_none(app, client):
    rv = client.get('/get')
    assert rv.data == b'None'

def test_get_value_set(app, client):
    client.get('/set/test_value')
    rv = client.get('/get')
    assert rv.data == b'test_value'

def test_get_value_nonascii(app, client):
    client.get('/set/\xe2\x9c\x94')  # Setting a non-ASCII value
    rv = client.get('/get')
    assert rv.data == b'\xe2\x9c\x94'  # Checking for the non-ASCII value

def test_get_value_empty(app, client):
    client.get('/set/')
    rv = client.get('/get')
    assert rv.data == b''  # Checking for empty string case

def test_get_value_after_clear(app, client):
    client.get('/set/test_value')
    with client.session_transaction() as sess:
        sess.clear()  # Clearing the session
    rv = client.get('/get')
    assert rv.data == b'None'  # Should return None after clearing session
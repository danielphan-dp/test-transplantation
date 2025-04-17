import flask
import pytest
from flask import Flask, session

app = Flask(__name__)
app.secret_key = 'test_secret'

@app.route('/get')
def get():
    v = flask.session.get('value', 'None')
    return v

def test_get_session_value_none():
    test_client = app.test_client()
    response = test_client.get('/get')
    assert response.data == b'None'

def test_get_session_value_set():
    with app.test_request_context():
        session['value'] = 'test_value'
    test_client = app.test_client()
    response = test_client.get('/get')
    assert response.data == b'test_value'

def test_get_session_value_empty_string():
    with app.test_request_context():
        session['value'] = ''
    test_client = app.test_client()
    response = test_client.get('/get')
    assert response.data == b''

def test_get_session_value_nonexistent_key():
    test_client = app.test_client()
    response = test_client.get('/get')
    assert response.data == b'None'
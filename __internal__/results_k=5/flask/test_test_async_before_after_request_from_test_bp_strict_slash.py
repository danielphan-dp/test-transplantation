import flask
import pytest
from flask import Flask, session

app = Flask(__name__)
app.secret_key = 'test_secret'

@app.route('/get')
def get():
    v = flask.session.get('value', 'None')
    return v

def test_get_with_no_session_value():
    test_client = app.test_client()
    response = test_client.get('/get')
    assert response.data == b'None'

def test_get_with_session_value():
    with app.test_request_context():
        session['value'] = 'test_value'
    test_client = app.test_client()
    response = test_client.get('/get')
    assert response.data == b'test_value'

def test_get_with_empty_session_value():
    with app.test_request_context():
        session['value'] = ''
    test_client = app.test_client()
    response = test_client.get('/get')
    assert response.data == b''

def test_get_with_none_session_value():
    with app.test_request_context():
        session['value'] = None
    test_client = app.test_client()
    response = test_client.get('/get')
    assert response.data == b'None'
import logging
import sys
import pytest
from io import StringIO
from flask import Flask, session

app = Flask(__name__)
app.secret_key = 'test_secret'

@app.route('/get')
def get():
    v = session.get('value', 'None')
    return v

def test_get_value_none(app, client):
    with app.test_request_context():
        response = client.get('/get')
        assert response.data == b'None'
        assert response.status_code == 200

def test_get_value_set(app, client):
    with app.test_request_context():
        with app.test_client() as client:
            with client.session_transaction() as sess:
                sess['value'] = 'test_value'
            response = client.get('/get')
            assert response.data == b'test_value'
            assert response.status_code == 200

def test_get_value_empty(app, client):
    with app.test_request_context():
        with app.test_client() as client:
            with client.session_transaction() as sess:
                sess['value'] = ''
            response = client.get('/get')
            assert response.data == b''
            assert response.status_code == 200

def test_get_value_none_with_no_session(app, client):
    with app.test_request_context():
        response = client.get('/get')
        assert response.data == b'None'
        assert response.status_code == 200

def test_get_value_invalid_type(app, client):
    with app.test_request_context():
        with app.test_client() as client:
            with client.session_transaction() as sess:
                sess['value'] = 12345
            response = client.get('/get')
            assert response.data == b'12345'
            assert response.status_code == 200
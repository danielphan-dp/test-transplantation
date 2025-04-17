import pytest
from flask import Flask, session

app = Flask(__name__)
app.secret_key = 'test_secret'

@app.route('/get')
def get():
    v = session.get('value', 'None')
    return v

def test_get_value_none():
    with app.test_client() as client:
        response = client.get('/get')
        assert response.data == b'None'

def test_get_value_set():
    with app.test_client() as client:
        with client.session_transaction() as sess:
            sess['value'] = 'test_value'
        response = client.get('/get')
        assert response.data == b'test_value'

def test_get_value_empty_string():
    with app.test_client() as client:
        with client.session_transaction() as sess:
            sess['value'] = ''
        response = client.get('/get')
        assert response.data == b''

def test_get_value_none_after_set():
    with app.test_client() as client:
        with client.session_transaction() as sess:
            sess['value'] = 'test_value'
        with client.session_transaction() as sess:
            sess.pop('value', None)
        response = client.get('/get')
        assert response.data == b'None'
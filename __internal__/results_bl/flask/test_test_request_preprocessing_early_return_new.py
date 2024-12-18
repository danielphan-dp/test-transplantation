import pytest
from flask import Flask, session

app = Flask(__name__)
app.secret_key = 'test_secret'

@app.route('/get')
def get():
    v = session.get('value', 'None')
    return v

def test_get_value_none(client):
    rv = client.get('/get')
    assert rv.data.strip() == b'None'

def test_get_value_set(client):
    with client.session_transaction() as sess:
        sess['value'] = 'test_value'
    rv = client.get('/get')
    assert rv.data.strip() == b'test_value'

def test_get_value_empty_string(client):
    with client.session_transaction() as sess:
        sess['value'] = ''
    rv = client.get('/get')
    assert rv.data.strip() == b''

def test_get_value_nonexistent(client):
    rv = client.get('/get')
    assert rv.data.strip() == b'None'
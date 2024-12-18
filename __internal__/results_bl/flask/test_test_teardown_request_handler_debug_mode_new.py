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
    assert rv.status_code == 200
    assert rv.data == b'None'

def test_get_value_set(client):
    with client.session_transaction() as sess:
        sess['value'] = 'test_value'
    rv = client.get('/get')
    assert rv.status_code == 200
    assert rv.data == b'test_value'

def test_get_value_empty(client):
    with client.session_transaction() as sess:
        sess['value'] = ''
    rv = client.get('/get')
    assert rv.status_code == 200
    assert rv.data == b''

def test_get_value_none_after_clear(client):
    with client.session_transaction() as sess:
        sess['value'] = 'test_value'
    with client.session_transaction() as sess:
        sess.clear()
    rv = client.get('/get')
    assert rv.status_code == 200
    assert rv.data == b'None'
import pytest
from flask import Flask, session

app = Flask(__name__)
app.secret_key = 'test_secret'

@app.route('/get')
def get():
    v = session.get('value', 'None')
    return v

def test_get_value_in_session(client):
    with client.session_transaction() as sess:
        sess['value'] = 'test_value'
    rv = client.get('/get')
    assert rv.data.decode() == 'test_value'

def test_get_value_not_in_session(client):
    rv = client.get('/get')
    assert rv.data.decode() == 'None'

def test_get_value_empty_string_in_session(client):
    with client.session_transaction() as sess:
        sess['value'] = ''
    rv = client.get('/get')
    assert rv.data.decode() == ''

def test_get_value_none_in_session(client):
    with client.session_transaction() as sess:
        sess['value'] = None
    rv = client.get('/get')
    assert rv.data.decode() == 'None'
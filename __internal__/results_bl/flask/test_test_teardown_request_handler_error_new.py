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
    assert rv.data == b'None'
    assert rv.status_code == 200

def test_get_value_set(client):
    with client.session_transaction() as sess:
        sess['value'] = 'test_value'
    rv = client.get('/get')
    assert rv.data == b'test_value'
    assert rv.status_code == 200

def test_get_value_empty(client):
    with client.session_transaction() as sess:
        sess['value'] = ''
    rv = client.get('/get')
    assert rv.data == b''
    assert rv.status_code == 200

def test_get_value_none_with_other_data(client):
    with client.session_transaction() as sess:
        sess['other_key'] = 'other_value'
    rv = client.get('/get')
    assert rv.data == b'None'
    assert rv.status_code == 200

def test_get_value_after_teardown_error(client):
    @app.teardown_request
    def teardown_request(exc):
        assert type(exc) is ZeroDivisionError

    @app.route("/")
    def fails():
        raise ZeroDivisionError

    rv = client.get("/")
    assert rv.status_code == 500
    assert b"Internal Server Error" in rv.data

    rv = client.get('/get')
    assert rv.data == b'None'
    assert rv.status_code == 200
import flask
import pytest

app = flask.Flask(__name__)

@app.route('/get')
def get():
    v = flask.session.get('value', 'None')
    return v

def test_get_value_none():
    client = app.test_client()
    with client.session_transaction() as session:
        session['value'] = None
    rv = client.get('/get')
    assert rv.data == b'None'

def test_get_value_set():
    client = app.test_client()
    with client.session_transaction() as session:
        session['value'] = 'test_value'
    rv = client.get('/get')
    assert rv.data == b'test_value'

def test_get_value_default():
    client = app.test_client()
    rv = client.get('/get')
    assert rv.data == b'None'

def test_get_value_empty_string():
    client = app.test_client()
    with client.session_transaction() as session:
        session['value'] = ''
    rv = client.get('/get')
    assert rv.data == b''

def test_get_value_integer():
    client = app.test_client()
    with client.session_transaction() as session:
        session['value'] = 123
    rv = client.get('/get')
    assert rv.data == b'123'

def test_get_value_boolean():
    client = app.test_client()
    with client.session_transaction() as session:
        session['value'] = True
    rv = client.get('/get')
    assert rv.data == b'True'
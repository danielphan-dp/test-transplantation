import flask
import pytest

app = flask.Flask(__name__)

@app.route('/get')
def get():
    v = flask.session.get('value', 'None')
    return v

def test_get_with_default_value():
    client = app.test_client()
    with client.session_transaction() as session:
        session['value'] = 'test_value'
    rv = client.get('/get')
    assert rv.data == b'test_value'

def test_get_with_none_value():
    client = app.test_client()
    with client.session_transaction() as session:
        session['value'] = None
    rv = client.get('/get')
    assert rv.data == b'None'

def test_get_without_value():
    client = app.test_client()
    rv = client.get('/get')
    assert rv.data == b'None'
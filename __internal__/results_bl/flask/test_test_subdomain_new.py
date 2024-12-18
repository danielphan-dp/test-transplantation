import flask
import pytest

app = flask.Flask(__name__)

@app.route('/get')
def get():
    v = flask.session.get('value', 'None')
    return v

def test_get_value_none():
    client = app.test_client()
    with client:
        response = client.get('/get')
    assert 200 == response.status_code
    assert b'None' == response.data

def test_get_value_set():
    client = app.test_client()
    with client:
        with flask.session_transaction() as session:
            session['value'] = 'test_value'
        response = client.get('/get')
    assert 200 == response.status_code
    assert b'test_value' == response.data

def test_get_value_empty_string():
    client = app.test_client()
    with client:
        with flask.session_transaction() as session:
            session['value'] = ''
        response = client.get('/get')
    assert 200 == response.status_code
    assert b'' == response.data

def test_get_value_none_after_clear():
    client = app.test_client()
    with client:
        with flask.session_transaction() as session:
            session.clear()
        response = client.get('/get')
    assert 200 == response.status_code
    assert b'None' == response.data
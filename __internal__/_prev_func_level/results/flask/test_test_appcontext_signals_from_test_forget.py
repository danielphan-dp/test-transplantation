import flask
import pytest

def test_get_value_none(app, client):
    with client.session_transaction() as session:
        session['value'] = None
    rv = client.get('/get')
    assert rv.data == b'None'

def test_get_value_set(app, client):
    with client.session_transaction() as session:
        session['value'] = 'test_value'
    rv = client.get('/get')
    assert rv.data == b'test_value'

def test_get_value_default(app, client):
    rv = client.get('/get')
    assert rv.data == b'None'

def test_get_value_empty_string(app, client):
    with client.session_transaction() as session:
        session['value'] = ''
    rv = client.get('/get')
    assert rv.data == b''

def test_get_value_integer(app, client):
    with client.session_transaction() as session:
        session['value'] = 123
    rv = client.get('/get')
    assert rv.data == b'123'
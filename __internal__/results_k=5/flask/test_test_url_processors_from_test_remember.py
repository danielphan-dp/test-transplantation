import flask
import pytest

def test_get_value_none(app, client):
    with client.session_transaction() as session:
        session['value'] = None
    response = client.get('/get')
    assert response.data == b'None'

def test_get_value_set(app, client):
    with client.session_transaction() as session:
        session['value'] = 'test_value'
    response = client.get('/get')
    assert response.data == b'test_value'

def test_get_value_default(app, client):
    response = client.get('/get')
    assert response.data == b'None'

def test_get_value_empty_string(app, client):
    with client.session_transaction() as session:
        session['value'] = ''
    response = client.get('/get')
    assert response.data == b''

def test_get_value_integer(app, client):
    with client.session_transaction() as session:
        session['value'] = 123
    response = client.get('/get')
    assert response.data == b'123'
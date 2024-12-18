import logging
import pytest
import flask
from blueprintapp.app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_get_with_default_value(client):
    rv = client.get('/get')
    assert rv.data == b'None'

def test_get_with_set_value(client):
    with client.session_transaction() as session:
        session['value'] = 'test_value'
    rv = client.get('/get')
    assert rv.data == b'test_value'

def test_get_with_empty_value(client):
    with client.session_transaction() as session:
        session['value'] = ''
    rv = client.get('/get')
    assert rv.data == b''

def test_get_with_none_value(client):
    with client.session_transaction() as session:
        session['value'] = None
    rv = client.get('/get')
    assert rv.data == b'None'
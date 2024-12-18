import logging
import pytest
import flask
from blueprintapp.app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_get_value_none(client):
    rv = client.get('/get')
    assert rv.data == b'None'

def test_get_value_set(client):
    with client.session_transaction() as session:
        session['value'] = 'TestValue'
    rv = client.get('/get')
    assert rv.data == b'TestValue'

def test_get_value_empty_string(client):
    with client.session_transaction() as session:
        session['value'] = ''
    rv = client.get('/get')
    assert rv.data == b''

def test_get_value_special_characters(client):
    with client.session_transaction() as session:
        session['value'] = 'Special@#&*'
    rv = client.get('/get')
    assert rv.data == b'Special@#&*'
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

def test_get_with_session_value(client):
    with client.session_transaction() as session:
        session['value'] = 'Test Value'
    rv = client.get('/get')
    assert rv.data == b'Test Value'

def test_get_with_boolean_value(client):
    with client.session_transaction() as session:
        session['value'] = True
    rv = client.get('/get')
    assert rv.data == b'True'

def test_get_with_none_value(client):
    with client.session_transaction() as session:
        session['value'] = None
    rv = client.get('/get')
    assert rv.data == b'None'
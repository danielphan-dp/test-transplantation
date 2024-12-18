import warnings
import pytest
import flask
from flask.testing import EnvironBuilder

@pytest.fixture
def client(app):
    return app.test_client()

def test_get_value_from_session(client):
    with client.session_transaction() as session:
        session['value'] = 'test_value'
    
    rv = client.get('/get')
    assert rv.data.decode() == 'test_value'

def test_get_value_not_set(client):
    rv = client.get('/get')
    assert rv.data.decode() == 'None'

def test_get_value_empty_string(client):
    with client.session_transaction() as session:
        session['value'] = ''
    
    rv = client.get('/get')
    assert rv.data.decode() == ''
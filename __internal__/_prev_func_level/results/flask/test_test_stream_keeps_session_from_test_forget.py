import flask
import pytest

def test_get_session_value_none(self, app, client):
    with client.session_transaction() as session:
        session['value'] = None
    rv = client.get('/get')
    assert rv.data == b'None'

def test_get_session_value_set(self, app, client):
    with client.session_transaction() as session:
        session['value'] = 'test_value'
    rv = client.get('/get')
    assert rv.data == b'test_value'

def test_get_session_value_default(self, app, client):
    rv = client.get('/get')
    assert rv.data == b'None'
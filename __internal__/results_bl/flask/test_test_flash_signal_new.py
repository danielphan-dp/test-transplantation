import flask
import pytest

def test_get_value_none(app):
    client = app.test_client()
    with client.session_transaction() as session:
        session.clear()
    response = client.get('/get')
    assert response.data.decode() == 'None'

def test_get_value_set(app):
    client = app.test_client()
    with client.session_transaction() as session:
        session['value'] = 'test_value'
    response = client.get('/get')
    assert response.data.decode() == 'test_value'

def test_get_value_empty_string(app):
    client = app.test_client()
    with client.session_transaction() as session:
        session['value'] = ''
    response = client.get('/get')
    assert response.data.decode() == ''
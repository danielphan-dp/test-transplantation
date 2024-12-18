import pytest
import flask

def test_get_value_none(app, client):
    with client:
        response = client.get('/get')
        assert response.data.decode() == 'None'

def test_get_value_set(app, client):
    with client:
        with client.session_transaction() as session:
            session['value'] = 'TestValue'
        response = client.get('/get')
        assert response.data.decode() == 'TestValue'

def test_get_value_empty_string(app, client):
    with client:
        with client.session_transaction() as session:
            session['value'] = ''
        response = client.get('/get')
        assert response.data.decode() == ''

def test_get_value_special_characters(app, client):
    with client:
        with client.session_transaction() as session:
            session['value'] = '!@#$%^&*()'
        response = client.get('/get')
        assert response.data.decode() == '!@#$%^&*()'
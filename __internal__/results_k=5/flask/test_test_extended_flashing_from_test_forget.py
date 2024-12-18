import flask
import pytest
from markupsafe import Markup

def test_get_value_none(app):
    client = app.test_client()
    response = client.get('/get')
    assert response.data.decode() == 'None'

def test_get_value_set(app):
    with app.test_request_context():
        flask.session['value'] = 'Test Value'
    client = app.test_client()
    response = client.get('/get')
    assert response.data.decode() == 'Test Value'

def test_get_value_empty_string(app):
    with app.test_request_context():
        flask.session['value'] = ''
    client = app.test_client()
    response = client.get('/get')
    assert response.data.decode() == ''

def test_get_value_special_characters(app):
    with app.test_request_context():
        flask.session['value'] = 'Special & Characters < > " \''
    client = app.test_client()
    response = client.get('/get')
    assert response.data.decode() == 'Special & Characters < > " \''

def test_get_value_after_clear(app):
    with app.test_request_context():
        flask.session['value'] = 'To be cleared'
        flask.session.clear()
    client = app.test_client()
    response = client.get('/get')
    assert response.data.decode() == 'None'
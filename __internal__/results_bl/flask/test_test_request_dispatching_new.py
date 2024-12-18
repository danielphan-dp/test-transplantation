import flask
import pytest

def test_get_value(app, client):
    with app.test_request_context():
        flask.session['value'] = 'test_value'
        response = client.get('/get')
        assert response.data == b'test_value'

def test_get_value_none(app, client):
    with app.test_request_context():
        response = client.get('/get')
        assert response.data == b'None'

def test_get_value_empty(app, client):
    with app.test_request_context():
        flask.session['value'] = ''
        response = client.get('/get')
        assert response.data == b''

def test_get_value_non_string(app, client):
    with app.test_request_context():
        flask.session['value'] = 12345
        response = client.get('/get')
        assert response.data == b'12345'
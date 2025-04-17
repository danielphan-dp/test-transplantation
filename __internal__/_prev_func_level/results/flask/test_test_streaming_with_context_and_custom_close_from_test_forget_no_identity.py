import flask
import pytest

def test_get_session_value_none(app, client):
    with app.test_request_context():
        flask.session['value'] = None
        response = client.get('/get')
        assert response.data == b'None'

def test_get_session_value_set(app, client):
    with app.test_request_context():
        flask.session['value'] = 'TestValue'
        response = client.get('/get')
        assert response.data == b'TestValue'

def test_get_session_value_default(app, client):
    with app.test_request_context():
        response = client.get('/get')
        assert response.data == b'None'

def test_get_session_value_empty_string(app, client):
    with app.test_request_context():
        flask.session['value'] = ''
        response = client.get('/get')
        assert response.data == b''

def test_get_session_value_integer(app, client):
    with app.test_request_context():
        flask.session['value'] = 123
        response = client.get('/get')
        assert response.data == b'123'
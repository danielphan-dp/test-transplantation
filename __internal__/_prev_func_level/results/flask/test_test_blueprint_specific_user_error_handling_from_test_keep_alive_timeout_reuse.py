import flask
import pytest

def test_get_value_from_session(app, client):
    with app.test_request_context():
        flask.session['value'] = 'test_value'
        response = client.get('/get')
        assert response.data == b'test_value'

def test_get_value_not_set_in_session(app, client):
    with app.test_request_context():
        response = client.get('/get')
        assert response.data == b'None'

def test_get_value_empty_string_in_session(app, client):
    with app.test_request_context():
        flask.session['value'] = ''
        response = client.get('/get')
        assert response.data == b''

def test_get_value_none_in_session(app, client):
    with app.test_request_context():
        flask.session['value'] = None
        response = client.get('/get')
        assert response.data == b'None'
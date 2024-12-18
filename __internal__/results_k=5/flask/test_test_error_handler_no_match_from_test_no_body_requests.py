import pytest
import flask

def test_get_method_with_session_value(app, client):
    with app.test_request_context():
        flask.session['value'] = 'test_value'
        response = client.get('/get')
        assert response.data == b'test_value'

def test_get_method_with_none_session_value(app, client):
    with app.test_request_context():
        flask.session.pop('value', None)
        response = client.get('/get')
        assert response.data == b'None'

def test_get_method_with_empty_session_value(app, client):
    with app.test_request_context():
        flask.session['value'] = ''
        response = client.get('/get')
        assert response.data == b''

def test_get_method_with_non_string_session_value(app, client):
    with app.test_request_context():
        flask.session['value'] = 12345
        response = client.get('/get')
        assert response.data == b'12345'
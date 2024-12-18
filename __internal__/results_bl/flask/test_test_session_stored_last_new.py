import flask
import pytest

def test_get_session_value_none(app, client):
    with app.test_request_context():
        flask.session.clear()
        response = client.get('/get')
        assert response.data == b'None'

def test_get_session_value_set(app, client):
    with app.test_request_context():
        flask.session['value'] = 'test_value'
        response = client.get('/get')
        assert response.data == b'test_value'

def test_get_session_value_empty_string(app, client):
    with app.test_request_context():
        flask.session['value'] = ''
        response = client.get('/get')
        assert response.data == b''

def test_get_session_value_none_after_clear(app, client):
    with app.test_request_context():
        flask.session['value'] = 'some_value'
        flask.session.clear()
        response = client.get('/get')
        assert response.data == b'None'
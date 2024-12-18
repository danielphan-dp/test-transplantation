import flask
import pytest

def test_get_method_with_session_value(app, client):
    with app.app_context():
        flask.session['value'] = 'test_value'
        response = client.get('/get')
        assert response.data == b'test_value'

def test_get_method_with_no_session_value(app, client):
    with app.app_context():
        response = client.get('/get')
        assert response.data == b'None'

def test_get_method_with_empty_session_value(app, client):
    with app.app_context():
        flask.session['value'] = ''
        response = client.get('/get')
        assert response.data == b''
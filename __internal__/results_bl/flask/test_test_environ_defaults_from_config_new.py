import pytest
import flask

def test_get_with_default_value(app, client):
    with app.test_request_context():
        flask.session['value'] = None
        response = client.get('/get')
        assert response.data == b'None'

def test_get_with_set_value(app, client):
    with app.test_request_context():
        flask.session['value'] = 'test_value'
        response = client.get('/get')
        assert response.data == b'test_value'

def test_get_with_empty_value(app, client):
    with app.test_request_context():
        flask.session['value'] = ''
        response = client.get('/get')
        assert response.data == b''

def test_get_with_nonexistent_value(app, client):
    with app.test_request_context():
        response = client.get('/get')
        assert response.data == b'None'
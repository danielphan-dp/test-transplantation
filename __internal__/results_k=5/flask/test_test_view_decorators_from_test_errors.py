import pytest
import flask

def test_get_value(app, client):
    with app.test_request_context():
        flask.session['value'] = 'Test Value'
        response = client.get('/get')
        assert response.data == b'Test Value'

def test_get_default_value(app, client):
    with app.test_request_context():
        response = client.get('/get')
        assert response.data == b'None'

def test_get_value_empty_session(app, client):
    with app.test_request_context():
        flask.session.clear()
        response = client.get('/get')
        assert response.data == b'None'

def test_get_value_none_type(app, client):
    with app.test_request_context():
        flask.session['value'] = None
        response = client.get('/get')
        assert response.data == b'None'
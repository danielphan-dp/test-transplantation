import pytest
import flask

def test_get_method_with_session_value(app, client):
    with app.test_request_context():
        flask.session['value'] = 'Test Value'
        response = client.get('/get')
        assert response.data == b'Test Value'

def test_get_method_with_none_value(app, client):
    with app.test_request_context():
        flask.session.pop('value', None)
        response = client.get('/get')
        assert response.data == b'None'

def test_get_method_with_empty_session(app, client):
    with app.test_request_context():
        flask.session.clear()
        response = client.get('/get')
        assert response.data == b'None'

def test_get_method_with_different_value(app, client):
    with app.test_request_context():
        flask.session['value'] = 'Another Value'
        response = client.get('/get')
        assert response.data == b'Another Value'
import pytest
import flask

def test_get_route_with_session_value(app):
    with app.test_request_context():
        flask.session['value'] = 'Test Value'
        response = app.test_client().get('/get')
        assert response.data.decode() == 'Test Value'

def test_get_route_with_none_session_value(app):
    with app.test_request_context():
        response = app.test_client().get('/get')
        assert response.data.decode() == 'None'

def test_get_route_with_empty_session_value(app):
    with app.test_request_context():
        flask.session['value'] = ''
        response = app.test_client().get('/get')
        assert response.data.decode() == ''

def test_get_route_without_session(app):
    with app.test_request_context():
        response = app.test_client().get('/get')
        assert response.data.decode() == 'None'
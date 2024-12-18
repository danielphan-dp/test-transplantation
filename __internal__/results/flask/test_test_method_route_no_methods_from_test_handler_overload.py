import pytest
import flask

def test_get_route_with_session_value(app):
    with app.test_request_context():
        flask.session['value'] = 'test_value'
        response = app.test_client().get('/get')
        assert response.data.decode() == 'test_value'

def test_get_route_with_no_session_value(app):
    with app.test_request_context():
        response = app.test_client().get('/get')
        assert response.data.decode() == 'None'

def test_get_route_with_empty_session_value(app):
    with app.test_request_context():
        flask.session['value'] = ''
        response = app.test_client().get('/get')
        assert response.data.decode() == ''

def test_get_route_with_none_session_value(app):
    with app.test_request_context():
        flask.session['value'] = None
        response = app.test_client().get('/get')
        assert response.data.decode() == 'None'
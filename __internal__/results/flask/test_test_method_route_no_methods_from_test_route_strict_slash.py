import pytest
import flask

def test_get_route_with_session_value(app):
    with app.test_client() as client:
        with flask.session_transaction() as session:
            session['value'] = 'Test Value'
        response = client.get('/get')
        assert response.data.decode() == 'Test Value'

def test_get_route_without_session_value(app):
    with app.test_client() as client:
        response = client.get('/get')
        assert response.data.decode() == 'None'

def test_get_route_with_empty_session_value(app):
    with app.test_client() as client:
        with flask.session_transaction() as session:
            session['value'] = ''
        response = client.get('/get')
        assert response.data.decode() == ''

def test_get_route_with_none_session_value(app):
    with app.test_client() as client:
        with flask.session_transaction() as session:
            session['value'] = None
        response = client.get('/get')
        assert response.data.decode() == 'None'
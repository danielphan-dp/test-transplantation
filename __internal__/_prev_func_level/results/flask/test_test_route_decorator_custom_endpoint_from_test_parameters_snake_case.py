import flask
import pytest

def test_get_route_with_session_value(app, client):
    with app.app_context():
        flask.session['value'] = 'test_value'
        response = client.get('/get')
        assert response.data == b'test_value'

def test_get_route_with_none_session_value(app, client):
    with app.app_context():
        flask.session.pop('value', None)
        response = client.get('/get')
        assert response.data == b'None'

def test_get_route_without_session(app, client):
    with app.app_context():
        response = client.get('/get')
        assert response.data == b'None'
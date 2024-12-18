import flask
import pytest

def test_get_session_value_none(self, app, client):
    with app.test_request_context():
        flask.session['value'] = None
        response = client.get('/get')
        assert response.data == b'None'

def test_get_session_value_set(self, app, client):
    with app.test_request_context():
        flask.session['value'] = 'test_value'
        response = client.get('/get')
        assert response.data == b'test_value'

def test_get_session_value_default(self, app, client):
    with app.test_request_context():
        response = client.get('/get')
        assert response.data == b'None'
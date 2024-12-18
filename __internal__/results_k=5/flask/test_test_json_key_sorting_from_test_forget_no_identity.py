import flask
import pytest

def test_get_session_value(app, client):
    with app.test_request_context():
        flask.session['value'] = 'test_value'
        response = client.get('/get')
        assert response.data.decode('utf-8') == 'test_value'

def test_get_session_value_default(app, client):
    with app.test_request_context():
        response = client.get('/get')
        assert response.data.decode('utf-8') == 'None'

def test_get_session_value_empty(app, client):
    with app.test_request_context():
        flask.session['value'] = ''
        response = client.get('/get')
        assert response.data.decode('utf-8') == ''
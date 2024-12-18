import pytest
import flask

def test_get_value_from_session(app, client):
    with app.test_request_context():
        flask.session['value'] = 'test_value'
        response = client.get('/get')
        assert response.data.decode() == 'test_value'

def test_get_value_not_set(app, client):
    with app.test_request_context():
        response = client.get('/get')
        assert response.data.decode() == 'None'

def test_get_value_empty_string(app, client):
    with app.test_request_context():
        flask.session['value'] = ''
        response = client.get('/get')
        assert response.data.decode() == ''

def test_get_value_none_type(app, client):
    with app.test_request_context():
        flask.session['value'] = None
        response = client.get('/get')
        assert response.data.decode() == 'None'
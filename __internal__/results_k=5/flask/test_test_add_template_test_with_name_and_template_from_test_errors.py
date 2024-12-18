import pytest
import flask

def test_get_value_from_session(app, client):
    with app.test_request_context():
        flask.session['value'] = 'Test Value'
        response = client.get('/get')
        assert response.data == b'Test Value'

def test_get_value_not_set_in_session(app, client):
    with app.test_request_context():
        response = client.get('/get')
        assert response.data == b'None'

def test_get_value_with_none_in_session(app, client):
    with app.test_request_context():
        flask.session['value'] = None
        response = client.get('/get')
        assert response.data == b'None'

def test_get_value_with_empty_string_in_session(app, client):
    with app.test_request_context():
        flask.session['value'] = ''
        response = client.get('/get')
        assert response.data == b''

def test_get_value_with_special_characters_in_session(app, client):
    with app.test_request_context():
        flask.session['value'] = 'Special!@#$%^&*()'
        response = client.get('/get')
        assert response.data == b'Special!@#$%^&*()'
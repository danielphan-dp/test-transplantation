import flask
import pytest

def test_get_value_from_session(app, client):
    with app.test_request_context():
        flask.session['value'] = 'test_value'
        response = client.get('/get')
        assert response.data == b'test_value'

def test_get_value_not_set(app, client):
    with app.test_request_context():
        response = client.get('/get')
        assert response.data == b'None'

def test_get_value_after_modification(app, client):
    with app.test_request_context():
        flask.session['value'] = 'initial_value'
        response = client.get('/get')
        assert response.data == b'initial_value'
        
        flask.session['value'] = 'modified_value'
        response = client.get('/get')
        assert response.data == b'modified_value'
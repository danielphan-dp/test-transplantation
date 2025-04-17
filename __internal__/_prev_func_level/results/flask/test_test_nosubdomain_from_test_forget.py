import flask
import pytest

def test_get_value_none(app, client):
    with app.test_request_context():
        flask.session['value'] = None
        response = client.get('/get')
        assert response.status_code == 200
        assert response.data == b'None'

def test_get_value_set(app, client):
    with app.test_request_context():
        flask.session['value'] = 'test_value'
        response = client.get('/get')
        assert response.status_code == 200
        assert response.data == b'test_value'

def test_get_value_default(app, client):
    with app.test_request_context():
        response = client.get('/get')
        assert response.status_code == 200
        assert response.data == b'None'
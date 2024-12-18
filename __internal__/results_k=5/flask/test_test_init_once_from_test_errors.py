import pytest
import flask

def test_get_value(app, client):
    with app.app_context():
        flask.session['value'] = 'test_value'
        response = client.get('/get')
        assert response.data == b'test_value'

def test_get_default_value(app, client):
    with app.app_context():
        response = client.get('/get')
        assert response.data == b'None'

def test_get_value_after_reset(app, client):
    with app.app_context():
        flask.session['value'] = 'initial_value'
        client.get('/get')  # Access to set the session
        flask.session.clear()  # Clear the session
        response = client.get('/get')
        assert response.data == b'None'

def test_get_value_with_multiple_requests(app, client):
    with app.app_context():
        flask.session['value'] = 'persistent_value'
        response1 = client.get('/get')
        response2 = client.get('/get')
        assert response1.data == b'persistent_value'
        assert response2.data == b'persistent_value'
import pytest
import flask

def test_get_value_from_session(app, client):
    with app.app_context():
        flask.session['value'] = 'test_value'
        response = client.get('/get')
        assert response.data.decode() == 'test_value'

def test_get_value_not_set_in_session(app, client):
    with app.app_context():
        response = client.get('/get')
        assert response.data.decode() == 'None'

def test_get_value_after_session_clear(app, client):
    with app.app_context():
        flask.session['value'] = 'test_value'
        client.get('/get')  # Access to set the session
        flask.session.clear()
        response = client.get('/get')
        assert response.data.decode() == 'None'
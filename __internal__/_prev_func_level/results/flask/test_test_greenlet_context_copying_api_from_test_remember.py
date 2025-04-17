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

def test_get_value_with_different_session_value(app, client):
    with app.test_request_context():
        flask.session['value'] = 'another_value'
        response = client.get('/get')
        assert response.data == b'another_value'

def test_get_value_after_session_clear(app, client):
    with app.test_request_context():
        flask.session['value'] = 'value_before_clear'
        flask.session.clear()
        response = client.get('/get')
        assert response.data == b'None'
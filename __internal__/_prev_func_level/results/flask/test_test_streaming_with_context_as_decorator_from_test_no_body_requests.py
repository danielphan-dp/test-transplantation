import flask
import pytest

def test_get_value_from_session(app, client):
    with app.test_request_context():
        flask.session['value'] = 'Test Value'
        response = client.get('/get')
        assert response.data == b'Test Value'

def test_get_value_from_session_default(app, client):
    response = client.get('/get')
    assert response.data == b'None'

def test_get_value_after_session_clear(app, client):
    with app.test_request_context():
        flask.session['value'] = 'Another Value'
        client.get('/get')
        flask.session.clear()
        response = client.get('/get')
        assert response.data == b'None'
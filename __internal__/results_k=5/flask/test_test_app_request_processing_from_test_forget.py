import pytest
import flask

def test_get_value_from_session(app, client):
    with app.test_request_context():
        flask.session['value'] = 'test_value'
        response = client.get('/get')
        assert response.data == b'test_value'

def test_get_value_not_set_in_session(app, client):
    with app.test_request_context():
        response = client.get('/get')
        assert response.data == b'None'

def test_get_value_after_setting_in_session(app, client):
    with app.test_request_context():
        flask.session['value'] = 'another_value'
        response = client.get('/get')
        assert response.data == b'another_value'

def test_get_value_with_multiple_requests(app, client):
    with app.test_request_context():
        flask.session['value'] = 'session_value'
        response1 = client.get('/get')
        assert response1.data == b'session_value'
        
        flask.session['value'] = 'updated_value'
        response2 = client.get('/get')
        assert response2.data == b'updated_value'
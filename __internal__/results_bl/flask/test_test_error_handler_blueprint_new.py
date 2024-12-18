import pytest
import flask

def test_get_method_with_no_session_value(app):
    c = app.test_client()
    response = c.get('/get')
    assert response.data == b'None'

def test_get_method_with_session_value(app):
    with app.test_request_context():
        flask.session['value'] = 'test_value'
    c = app.test_client()
    response = c.get('/get')
    assert response.data == b'test_value'

def test_get_method_with_empty_session_value(app):
    with app.test_request_context():
        flask.session['value'] = ''
    c = app.test_client()
    response = c.get('/get')
    assert response.data == b''
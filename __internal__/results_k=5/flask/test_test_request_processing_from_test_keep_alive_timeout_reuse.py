import flask
import pytest

def test_get_value_from_session(app, client):
    with app.test_request_context():
        flask.session['value'] = 'test_value'
        response = client.get('/get')
        assert response.data == b'test_value'

def test_get_value_not_set_in_session(app, client):
    response = client.get('/get')
    assert response.data == b'None'

def test_get_value_after_setting_in_session(app, client):
    with app.test_request_context():
        flask.session['value'] = 'another_value'
    response = client.get('/get')
    assert response.data == b'another_value'

def test_get_value_with_empty_session(app, client):
    with app.test_request_context():
        flask.session.clear()
    response = client.get('/get')
    assert response.data == b'None'
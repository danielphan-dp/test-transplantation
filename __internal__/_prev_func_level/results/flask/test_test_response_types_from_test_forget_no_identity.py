import flask
import pytest

def test_get_value_from_session(app, client):
    with app.test_request_context():
        flask.session['value'] = 'Test Value'
        rv = client.get('/get')
        assert rv.data.decode() == 'Test Value'

def test_get_value_not_set(app, client):
    with app.test_request_context():
        rv = client.get('/get')
        assert rv.data.decode() == 'None'

def test_get_value_empty_string(app, client):
    with app.test_request_context():
        flask.session['value'] = ''
        rv = client.get('/get')
        assert rv.data.decode() == ''

def test_get_value_none_type(app, client):
    with app.test_request_context():
        flask.session['value'] = None
        rv = client.get('/get')
        assert rv.data.decode() == 'None'
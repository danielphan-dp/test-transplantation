import flask
import pytest

def test_get_value_from_session(app, client):
    with app.test_request_context():
        flask.session['value'] = 'test_value'
        rv = client.get('/get')
        assert rv.data == b'test_value'

def test_get_value_not_set_in_session(app, client):
    with app.test_request_context():
        rv = client.get('/get')
        assert rv.data == b'None'

def test_get_value_with_none_in_session(app, client):
    with app.test_request_context():
        flask.session['value'] = None
        rv = client.get('/get')
        assert rv.data == b'None'
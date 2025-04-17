import flask
import pytest

def test_get_session_value_none(self, app, client):
    with app.test_request_context():
        flask.session['value'] = None
        rv = client.get('/get')
        assert rv.data == b'None'

def test_get_session_value_set(self, app, client):
    with app.test_request_context():
        flask.session['value'] = 'TestValue'
        rv = client.get('/get')
        assert rv.data == b'TestValue'

def test_get_session_value_default(self, app, client):
    with app.test_request_context():
        rv = client.get('/get')
        assert rv.data == b'None'
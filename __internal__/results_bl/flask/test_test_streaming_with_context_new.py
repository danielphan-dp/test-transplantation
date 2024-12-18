import pytest
import flask

def test_get_value_from_session(self, app, client):
    with app.app_context():
        flask.session['value'] = 'TestValue'
        rv = client.get('/get')
        assert rv.data == b'TestValue'

def test_get_value_not_set(self, app, client):
    with app.app_context():
        rv = client.get('/get')
        assert rv.data == b'None'

def test_get_value_empty_string(self, app, client):
    with app.app_context():
        flask.session['value'] = ''
        rv = client.get('/get')
        assert rv.data == b''

def test_get_value_none(self, app, client):
    with app.app_context():
        flask.session['value'] = None
        rv = client.get('/get')
        assert rv.data == b'None'
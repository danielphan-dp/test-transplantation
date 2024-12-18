import io
import os
import pytest
import werkzeug.exceptions
import flask
from flask.helpers import get_debug_flag
from flask.views import MethodView

def test_get_value_from_session(self, app, client):
    with app.test_request_context():
        flask.session['value'] = 'test_value'
        rv = client.get('/get')
        assert rv.data == b'test_value'

def test_get_value_not_set(self, app, client):
    with app.test_request_context():
        rv = client.get('/get')
        assert rv.data == b'None'

def test_get_value_empty_string(self, app, client):
    with app.test_request_context():
        flask.session['value'] = ''
        rv = client.get('/get')
        assert rv.data == b''

def test_get_value_none(self, app, client):
    with app.test_request_context():
        flask.session['value'] = None
        rv = client.get('/get')
        assert rv.data == b'None'
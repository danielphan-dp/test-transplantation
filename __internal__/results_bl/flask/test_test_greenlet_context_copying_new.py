import warnings
import pytest
import flask
from flask.globals import request_ctx
from flask.sessions import SecureCookieSessionInterface
from flask.sessions import SessionInterface
from greenlet import greenlet
from flask.testing import EnvironBuilder

def test_get_method_with_default_value(self, app, client):
    rv = client.get('/get')
    assert rv.data == b'None'

def test_get_method_with_session_value(self, app, client):
    with app.app_context():
        flask.session['value'] = 'test_value'
    rv = client.get('/get')
    assert rv.data == b'test_value'

def test_get_method_with_empty_session(self, app, client):
    with app.app_context():
        flask.session.clear()
    rv = client.get('/get')
    assert rv.data == b'None'

def test_get_method_with_none_value(self, app, client):
    with app.app_context():
        flask.session['value'] = None
    rv = client.get('/get')
    assert rv.data == b'None'
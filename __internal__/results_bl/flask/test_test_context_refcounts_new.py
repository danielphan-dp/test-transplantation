import pytest
import flask
from flask.globals import app_ctx, request_ctx

def test_get_value_none(app, client):
    with app_ctx:
        with request_ctx:
            flask.session['value'] = None
            res = client.get('/get')
            assert res.status_code == 200
            assert res.data == b'None'

def test_get_value_set(app, client):
    with app_ctx:
        with request_ctx:
            flask.session['value'] = 'test_value'
            res = client.get('/get')
            assert res.status_code == 200
            assert res.data == b'test_value'

def test_get_value_default(app, client):
    with app_ctx:
        with request_ctx:
            res = client.get('/get')
            assert res.status_code == 200
            assert res.data == b'None'
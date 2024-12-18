import flask
import pytest

def test_get_value_none(app, client):
    with app.test_request_context():
        flask.session['value'] = None
        rv = client.get('/get')
        assert rv.data.decode() == 'None'

def test_get_value_string(app, client):
    with app.test_request_context():
        flask.session['value'] = 'Hello'
        rv = client.get('/get')
        assert rv.data.decode() == 'Hello'

def test_get_value_integer(app, client):
    with app.test_request_context():
        flask.session['value'] = 42
        rv = client.get('/get')
        assert rv.data.decode() == '42'

def test_get_value_float(app, client):
    with app.test_request_context():
        flask.session['value'] = 3.14
        rv = client.get('/get')
        assert rv.data.decode() == '3.14'

def test_get_value_boolean(app, client):
    with app.test_request_context():
        flask.session['value'] = True
        rv = client.get('/get')
        assert rv.data.decode() == 'True'

def test_get_value_empty_string(app, client):
    with app.test_request_context():
        flask.session['value'] = ''
        rv = client.get('/get')
        assert rv.data.decode() == ''
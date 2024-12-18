import pytest
import flask

def test_get_value_none(app, client):
    with app.test_request_context():
        flask.session['value'] = None
        rv = client.get('/get')
        assert rv.data.decode('utf-8') == 'None'

def test_get_value_set(app, client):
    with app.test_request_context():
        flask.session['value'] = 'test_value'
        rv = client.get('/get')
        assert rv.data.decode('utf-8') == 'test_value'

def test_get_value_empty_string(app, client):
    with app.test_request_context():
        flask.session['value'] = ''
        rv = client.get('/get')
        assert rv.data.decode('utf-8') == ''

def test_get_value_integer(app, client):
    with app.test_request_context():
        flask.session['value'] = 123
        rv = client.get('/get')
        assert rv.data.decode('utf-8') == '123'

def test_get_value_float(app, client):
    with app.test_request_context():
        flask.session['value'] = 123.45
        rv = client.get('/get')
        assert rv.data.decode('utf-8') == '123.45'
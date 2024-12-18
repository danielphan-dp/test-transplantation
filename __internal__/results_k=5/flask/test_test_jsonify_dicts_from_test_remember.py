import flask
import pytest

def test_get_value_none(app, client):
    with app.test_request_context():
        flask.session['value'] = None
        rv = client.get('/get')
        assert rv.data == b'None'

def test_get_value_string(app, client):
    with app.test_request_context():
        flask.session['value'] = 'Hello'
        rv = client.get('/get')
        assert rv.data == b'Hello'

def test_get_value_integer(app, client):
    with app.test_request_context():
        flask.session['value'] = 42
        rv = client.get('/get')
        assert rv.data == b'42'

def test_get_value_float(app, client):
    with app.test_request_context():
        flask.session['value'] = 3.14
        rv = client.get('/get')
        assert rv.data == b'3.14'

def test_get_value_boolean(app, client):
    with app.test_request_context():
        flask.session['value'] = True
        rv = client.get('/get')
        assert rv.data == b'True'

def test_get_value_empty_string(app, client):
    with app.test_request_context():
        flask.session['value'] = ''
        rv = client.get('/get')
        assert rv.data == b''

def test_get_value_list(app, client):
    with app.test_request_context():
        flask.session['value'] = ['item1', 'item2']
        rv = client.get('/get')
        assert rv.data == b'None'  # Lists are not directly serializable to string

def test_get_value_dict(app, client):
    with app.test_request_context():
        flask.session['value'] = {'key': 'value'}
        rv = client.get('/get')
        assert rv.data == b'None'  # Dicts are not directly serializable to string

def test_get_value_unset(app, client):
    with app.test_request_context():
        rv = client.get('/get')
        assert rv.data == b'None'
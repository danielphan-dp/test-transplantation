import flask
import pytest

def test_get_value_none(app, client):
    with app.test_request_context():
        flask.session['value'] = None
        rv = client.get('/get')
        assert rv.data == b'None'

def test_get_value_set(app, client):
    with app.test_request_context():
        flask.session['value'] = 'test_value'
        rv = client.get('/get')
        assert rv.data == b'test_value'

def test_get_value_empty_string(app, client):
    with app.test_request_context():
        flask.session['value'] = ''
        rv = client.get('/get')
        assert rv.data == b''

def test_get_value_non_string(app, client):
    with app.test_request_context():
        flask.session['value'] = 12345
        rv = client.get('/get')
        assert rv.data == b'12345'

def test_get_value_boolean(app, client):
    with app.test_request_context():
        flask.session['value'] = True
        rv = client.get('/get')
        assert rv.data == b'True'

def test_get_value_list(app, client):
    with app.test_request_context():
        flask.session['value'] = ['item1', 'item2']
        rv = client.get('/get')
        assert rv.data == b"['item1', 'item2']"

def test_get_value_dict(app, client):
    with app.test_request_context():
        flask.session['value'] = {'key': 'value'}
        rv = client.get('/get')
        assert rv.data == b"{'key': 'value'}"
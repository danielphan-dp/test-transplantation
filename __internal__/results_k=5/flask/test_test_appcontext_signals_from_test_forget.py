import flask
import pytest

def test_get_value_none(app, client):
    rv = client.get('/get')
    assert rv.data == b'None'

def test_get_value_set(app, client):
    with app.app_context():
        flask.session['value'] = 'test_value'
    rv = client.get('/get')
    assert rv.data == b'test_value'

def test_get_value_empty_string(app, client):
    with app.app_context():
        flask.session['value'] = ''
    rv = client.get('/get')
    assert rv.data == b''

def test_get_value_nonexistent_key(app, client):
    rv = client.get('/get')
    assert rv.data == b'None'
import flask
import pytest

def test_get_value_from_session(app, client):
    with app.app_context():
        flask.session['value'] = 'test_value'
        rv = client.get('/get')
        assert rv.data.decode() == 'test_value'

def test_get_value_not_in_session(app, client):
    with app.app_context():
        rv = client.get('/get')
        assert rv.data.decode() == 'None'

def test_get_value_empty_string_in_session(app, client):
    with app.app_context():
        flask.session['value'] = ''
        rv = client.get('/get')
        assert rv.data.decode() == ''
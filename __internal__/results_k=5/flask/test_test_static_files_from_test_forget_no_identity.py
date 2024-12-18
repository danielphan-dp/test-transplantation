import flask
import pytest

def test_get_value_from_session(app, client):
    with app.test_request_context():
        flask.session['value'] = 'test_value'
        rv = client.get('/get')
        assert rv.data.decode() == 'test_value'
        assert rv.status_code == 200

def test_get_value_not_set(app, client):
    with app.test_request_context():
        rv = client.get('/get')
        assert rv.data.decode() == 'None'
        assert rv.status_code == 200

def test_get_value_empty_string(app, client):
    with app.test_request_context():
        flask.session['value'] = ''
        rv = client.get('/get')
        assert rv.data.decode() == ''
        assert rv.status_code == 200

def test_get_value_none(app, client):
    with app.test_request_context():
        flask.session['value'] = None
        rv = client.get('/get')
        assert rv.data.decode() == 'None'
        assert rv.status_code == 200
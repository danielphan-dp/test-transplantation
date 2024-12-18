import flask
import pytest

def test_get_with_default_value(app, client):
    with app.test_request_context():
        flask.session['value'] = None
        rv = client.get('/get')
        assert rv.data == b'None'

def test_get_with_set_value(app, client):
    with app.test_request_context():
        flask.session['value'] = 'test_value'
        rv = client.get('/get')
        assert rv.data == b'test_value'

def test_get_with_no_value_in_session(app, client):
    with app.test_request_context():
        if 'value' in flask.session:
            del flask.session['value']
        rv = client.get('/get')
        assert rv.data == b'None'
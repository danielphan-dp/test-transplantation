import flask
import pytest

def test_get_value_from_session():
    app = flask.Flask(__name__)
    client = app.test_client()

    with app.app_context():
        flask.session['value'] = 'test_value'
        rv = client.get('/get')
        assert rv.data == b'test_value'

def test_get_value_not_set_in_session():
    app = flask.Flask(__name__)
    client = app.test_client()

    with app.app_context():
        rv = client.get('/get')
        assert rv.data == b'None'

def test_get_value_with_different_session_value():
    app = flask.Flask(__name__)
    client = app.test_client()

    with app.app_context():
        flask.session['value'] = 'another_value'
        rv = client.get('/get')
        assert rv.data == b'another_value'

def test_get_value_after_session_clear():
    app = flask.Flask(__name__)
    client = app.test_client()

    with app.app_context():
        flask.session['value'] = 'value_before_clear'
        flask.session.clear()
        rv = client.get('/get')
        assert rv.data == b'None'
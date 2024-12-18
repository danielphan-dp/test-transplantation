import pytest
import flask

def test_get_value_from_session(app):
    with app.test_client() as c:
        with flask.session_transaction() as sess:
            sess['value'] = 'test_value'
        response = c.get('/get')
        assert response.data == b'test_value'

def test_get_value_not_set(app):
    with app.test_client() as c:
        response = c.get('/get')
        assert response.data == b'None'

def test_get_value_empty_string(app):
    with app.test_client() as c:
        with flask.session_transaction() as sess:
            sess['value'] = ''
        response = c.get('/get')
        assert response.data == b''

def test_get_value_none(app):
    with app.test_client() as c:
        with flask.session_transaction() as sess:
            sess['value'] = None
        response = c.get('/get')
        assert response.data == b'None'
import flask
import pytest

def test_get_method_with_session_value(app):
    with app.test_client() as c:
        with flask.session_transaction() as session:
            session['value'] = 'test_value'
        response = c.get('/get')
        assert response.data == b'test_value'

def test_get_method_with_no_session_value(app):
    with app.test_client() as c:
        response = c.get('/get')
        assert response.data == b'None'

def test_get_method_with_empty_session_value(app):
    with app.test_client() as c:
        with flask.session_transaction() as session:
            session['value'] = ''
        response = c.get('/get')
        assert response.data == b''
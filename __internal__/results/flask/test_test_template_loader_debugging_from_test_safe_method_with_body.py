import flask
import pytest

def test_get_method_with_session_value(app, client):
    with app.test_client() as c:
        with flask.session_transaction() as sess:
            sess['value'] = 'Test Value'
        response = c.get('/get')
        assert response.data.decode('utf-8') == 'Test Value'

def test_get_method_with_no_session_value(app, client):
    with app.test_client() as c:
        response = c.get('/get')
        assert response.data.decode('utf-8') == 'None'

def test_get_method_with_empty_session_value(app, client):
    with app.test_client() as c:
        with flask.session_transaction() as sess:
            sess['value'] = ''
        response = c.get('/get')
        assert response.data.decode('utf-8') == ''
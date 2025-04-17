import flask
import pytest

def test_get_value_from_session(app, client):
    with app.test_client() as c:
        with flask.session_transaction() as session:
            session['value'] = 'test_value'
        
        response = c.get('/get')
        assert response.data.decode() == 'test_value'

def test_get_value_not_set(app, client):
    with app.test_client() as c:
        response = c.get('/get')
        assert response.data.decode() == 'None'

def test_get_value_empty_string(app, client):
    with app.test_client() as c:
        with flask.session_transaction() as session:
            session['value'] = ''
        
        response = c.get('/get')
        assert response.data.decode() == ''
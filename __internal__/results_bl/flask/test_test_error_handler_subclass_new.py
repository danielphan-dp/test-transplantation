import pytest
from flask import Flask, session

@pytest.fixture
def app():
    app = Flask(__name__)
    app.secret_key = 'test_secret'
    
    @app.route('/get')
    def get():
        v = session.get('value', 'None')
        return v
    
    return app

def test_get_value_none(app):
    with app.test_client() as c:
        response = c.get('/get')
        assert response.data == b'None'

def test_get_value_set(app):
    with app.test_client() as c:
        with c.session_transaction() as sess:
            sess['value'] = 'test_value'
        response = c.get('/get')
        assert response.data == b'test_value'

def test_get_value_empty_string(app):
    with app.test_client() as c:
        with c.session_transaction() as sess:
            sess['value'] = ''
        response = c.get('/get')
        assert response.data == b''

def test_get_value_none_after_clear(app):
    with app.test_client() as c:
        with c.session_transaction() as sess:
            sess['value'] = 'test_value'
        with c.session_transaction() as sess:
            sess.clear()
        response = c.get('/get')
        assert response.data == b'None'
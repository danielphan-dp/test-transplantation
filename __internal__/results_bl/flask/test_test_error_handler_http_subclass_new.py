import pytest
from werkzeug.exceptions import Forbidden
from flask import Flask, session

@pytest.fixture
def app():
    app = Flask(__name__)
    app.secret_key = 'test_secret'
    return app

@app.route('/get')
def get():
    v = session.get('value', 'None')
    return v

def test_get_default_value(app):
    with app.test_client() as c:
        response = c.get('/get')
        assert response.data == b'None'

def test_get_with_value(app):
    with app.test_client() as c:
        with c.session_transaction() as sess:
            sess['value'] = 'test_value'
        response = c.get('/get')
        assert response.data == b'test_value'

def test_get_with_none_value(app):
    with app.test_client() as c:
        with c.session_transaction() as sess:
            sess['value'] = None
        response = c.get('/get')
        assert response.data == b'None'
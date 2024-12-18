import pytest
import flask
from flask import Flask, session

@pytest.fixture
def app():
    app = Flask(__name__)
    app.secret_key = 'test_secret'
    return app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.mark.parametrize(('value', 'expected'), [
    ('test_value', 'test_value'),
    (None, 'None'),
    ('', ''),
])
def test_get_session_value(app, client, value, expected):
    with app.app_context():
        session['value'] = value
    response = client.get('/get')
    assert response.data.decode() == expected

def test_get_session_value_no_value(app, client):
    response = client.get('/get')
    assert response.data.decode() == 'None'
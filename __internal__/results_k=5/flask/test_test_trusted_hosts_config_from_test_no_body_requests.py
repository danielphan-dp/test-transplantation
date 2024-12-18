import flask
import pytest
from flask import Flask

@pytest.fixture
def app():
    app = Flask(__name__)
    app.secret_key = 'test_secret'
    return app

@app.route('/set')
def set_value():
    flask.session['value'] = 'test_value'
    return 'Value set'

def test_get_value(app):
    client = app.test_client()
    client.get('/set')
    
    response = client.get('/get')
    assert response.data.decode() == 'test_value'

def test_get_value_default(app):
    client = app.test_client()
    
    response = client.get('/get')
    assert response.data.decode() == 'None'

def test_get_value_after_clear(app):
    client = app.test_client()
    client.get('/set')
    with client.session_transaction() as session:
        session.clear()
    
    response = client.get('/get')
    assert response.data.decode() == 'None'
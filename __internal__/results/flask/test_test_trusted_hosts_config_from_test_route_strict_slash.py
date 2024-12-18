import flask
import pytest
from flask import Flask

@pytest.fixture
def app():
    app = Flask(__name__)
    app.secret_key = 'test_secret'
    return app

@app.route('/set', methods=['POST'])
def set_value():
    flask.session['value'] = 'test_value'
    return '', 204

def test_get_value(app):
    client = app.test_client()
    
    # Test default session value
    response = client.get('/get')
    assert response.data == b'None'
    
    # Set a session value and test retrieval
    client.post('/set')
    response = client.get('/get')
    assert response.data == b'test_value'
    
    # Test session value after clearing session
    with client.session_transaction() as session:
        session.clear()
    response = client.get('/get')
    assert response.data == b'None'
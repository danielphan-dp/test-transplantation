import pytest
from flask import Flask, session

app = Flask(__name__)
app.secret_key = 'test_secret'

@app.route('/get')
def get():
    v = session.get('value', 'None')
    return v

def test_get_value_none(app, client):
    response = client.get('/get')
    assert response.data.decode() == 'None'

def test_get_value_set(app, client):
    with app.test_request_context():
        session['value'] = 'test_value'
        response = client.get('/get')
        assert response.data.decode() == 'test_value'

def test_get_value_empty_string(app, client):
    with app.test_request_context():
        session['value'] = ''
        response = client.get('/get')
        assert response.data.decode() == ''

def test_get_value_nonexistent_key(app, client):
    with app.test_request_context():
        session.clear()
        response = client.get('/get')
        assert response.data.decode() == 'None'
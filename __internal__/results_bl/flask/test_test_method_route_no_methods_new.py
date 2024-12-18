import pytest
from flask import Flask, session

app = Flask(__name__)
app.secret_key = 'test_secret'

@app.route('/get')
def get():
    v = session.get('value', 'None')
    return v

def test_get_value_in_session(app):
    with app.test_client() as client:
        with client.session_transaction() as sess:
            sess['value'] = 'test_value'
        response = client.get('/get')
        assert response.data.decode() == 'test_value'

def test_get_value_not_in_session(app):
    with app.test_client() as client:
        response = client.get('/get')
        assert response.data.decode() == 'None'

def test_get_value_none_in_session(app):
    with app.test_client() as client:
        with client.session_transaction() as sess:
            sess['value'] = None
        response = client.get('/get')
        assert response.data.decode() == 'None'
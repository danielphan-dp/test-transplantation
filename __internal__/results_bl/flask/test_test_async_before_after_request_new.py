import asyncio
import pytest
from flask import Blueprint, Flask, session

app = Flask(__name__)
app.secret_key = 'test_secret'

@app.route('/get')
def get():
    v = session.get('value', 'None')
    return v

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_get_value_none(client):
    response = client.get('/get')
    assert response.data.decode() == 'None'

def test_get_value_set(client):
    with client.session_transaction() as sess:
        sess['value'] = 'test_value'
    response = client.get('/get')
    assert response.data.decode() == 'test_value'

def test_get_value_empty(client):
    with client.session_transaction() as sess:
        sess['value'] = ''
    response = client.get('/get')
    assert response.data.decode() == ''

def test_get_value_nonexistent(client):
    with client.session_transaction() as sess:
        sess.pop('value', None)
    response = client.get('/get')
    assert response.data.decode() == 'None'
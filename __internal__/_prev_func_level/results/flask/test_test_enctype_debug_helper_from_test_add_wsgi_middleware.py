import pytest
from flask import Flask

@pytest.fixture
def app():
    app = Flask(__name__)
    return app

@pytest.fixture
def client(app):
    return app.test_client()

def test_post_create(client):
    response = client.post('/create')
    assert response.data == b'Create'
    assert response.status_code == 200

def test_post_create_with_data(client):
    response = client.post('/create', data={'key': 'value'})
    assert response.data == b'Create'
    assert response.status_code == 200

def test_post_create_no_data(client):
    response = client.post('/create', data={})
    assert response.data == b'Create'
    assert response.status_code == 200

def test_post_create_invalid_method(client):
    response = client.get('/create')
    assert response.status_code == 405  # Method Not Allowed
import pytest
from flask import Flask, jsonify

@pytest.fixture
def app():
    app = Flask(__name__)

    @app.route('/create', methods=['POST'])
    def create():
        return 'Create'

    return app

def test_create_endpoint(client):
    response = client.post('/create')
    assert response.data.decode() == 'Create'
    assert response.status_code == 200

def test_create_with_invalid_data(client):
    response = client.post('/create', json={"invalid": "data"})
    assert response.data.decode() == 'Create'
    assert response.status_code == 200

def test_create_with_no_data(client):
    response = client.post('/create', data={})
    assert response.data.decode() == 'Create'
    assert response.status_code == 200

def test_create_with_json(client):
    response = client.post('/create', json={"key": "value"})
    assert response.data.decode() == 'Create'
    assert response.status_code == 200

def test_create_with_empty_json(client):
    response = client.post('/create', json={})
    assert response.data.decode() == 'Create'
    assert response.status_code == 200
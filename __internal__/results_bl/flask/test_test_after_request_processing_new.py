import pytest
from flask import Flask, session

@pytest.fixture
def client():
    app = Flask(__name__)
    app.secret_key = 'test_secret'
    
    @app.route('/get')
    def get():
        v = session.get('value', 'None')
        return v

    with app.test_client() as client:
        yield client

def test_get_value_none(client):
    response = client.get('/get')
    assert response.data.decode() == 'None'
    assert response.status_code == 200

def test_get_value_set(client):
    with client.session_transaction() as sess:
        sess['value'] = 'test_value'
    response = client.get('/get')
    assert response.data.decode() == 'test_value'
    assert response.status_code == 200

def test_get_value_empty(client):
    with client.session_transaction() as sess:
        sess['value'] = ''
    response = client.get('/get')
    assert response.data.decode() == ''
    assert response.status_code == 200

def test_get_value_none_with_other_data(client):
    with client.session_transaction() as sess:
        sess['other_key'] = 'other_value'
    response = client.get('/get')
    assert response.data.decode() == 'None'
    assert response.status_code == 200
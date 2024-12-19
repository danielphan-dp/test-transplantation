import pytest
from sanic import Sanic
from sanic.response import text

app = Sanic("TestApp")

@app.post("/scale")
def post(request):
    return text('I am post method')

@pytest.fixture
def http_client():
    return app.test_client

def test_post_method_success(http_client):
    _, response = http_client.post("/scale")
    assert response.status == 200
    assert response.text == 'I am post method'

def test_post_method_with_invalid_data(http_client):
    _, response = http_client.post("/scale", json={"replicas": "invalid"})
    assert response.status == 400

def test_post_method_empty_request(http_client):
    _, response = http_client.post("/scale", json={})
    assert response.status == 400

def test_post_method_missing_key(http_client):
    _, response = http_client.post("/scale", json={"replica": 4})
    assert response.status == 400

def test_post_method_large_replicas(http_client):
    _, response = http_client.post("/scale", json={"replicas": 1000})
    assert response.status == 200
    assert response.text == 'I am post method'
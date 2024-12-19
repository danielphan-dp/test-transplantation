import pytest
from sanic import Sanic
from sanic.response import text

app = Sanic("TestApp")

@app.post("/post")
def post(request):
    return text('I am post method')

@pytest.fixture
def http_client():
    return app.test_client

def test_post_method_success(http_client):
    _, response = http_client.post("/post")
    assert response.status == 200
    assert response.text == 'I am post method'

def test_post_method_with_data(http_client):
    _, response = http_client.post("/post", json={"data": "test"})
    assert response.status == 200
    assert response.text == 'I am post method'

def test_post_method_empty_request(http_client):
    _, response = http_client.post("/post", json={})
    assert response.status == 200
    assert response.text == 'I am post method'

def test_post_method_invalid_route(http_client):
    _, response = http_client.post("/invalid")
    assert response.status == 404

def test_post_method_with_large_payload(http_client):
    large_payload = {"data": "x" * 10000}
    _, response = http_client.post("/post", json=large_payload)
    assert response.status == 200
    assert response.text == 'I am post method'
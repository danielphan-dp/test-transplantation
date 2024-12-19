import pytest
from sanic import Sanic
from sanic.response import text

app = Sanic("TestApp")

@app.post("/test_post")
def post(request):
    return text('I am post method')

@pytest.fixture
def http_client():
    return app.test_client

def test_post_method_success(http_client):
    request, response = http_client.post("/test_post")
    assert response.status == 200
    assert response.text == 'I am post method'

def test_post_method_invalid_route(http_client):
    request, response = http_client.post("/invalid_route")
    assert response.status == 404

def test_post_method_with_data(http_client):
    request, response = http_client.post("/test_post", json={"key": "value"})
    assert response.status == 200
    assert response.text == 'I am post method'
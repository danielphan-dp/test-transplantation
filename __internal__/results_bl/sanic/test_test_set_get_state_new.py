import pytest
from sanic import Sanic
from sanic.response import text

app = Sanic("TestApp")

@app.get("/")
def get(request):
    return text('I am get method')

def test_get_method_valid_request(client):
    request, response = client.get("/")
    assert response.status == 200
    assert response.text == 'I am get method'

def test_get_method_invalid_request(client):
    request, response = client.get("/invalid")
    assert response.status == 404

def test_get_method_with_query_params(client):
    request, response = client.get("/?param=test")
    assert response.status == 200
    assert response.text == 'I am get method'  # Assuming the method does not change behavior with params

def test_get_method_empty_request(client):
    request, response = client.get("/")
    assert response.status == 200
    assert response.text == 'I am get method'
import pytest
from sanic import Sanic
from sanic.response import text

app = Sanic("test_get_method")

@app.get("/get")
def get_method(request):
    return text('I am get method')

def test_get_method_returns_correct_text():
    request, response = app.test_client.get("/get")
    assert response.text == 'I am get method'

def test_get_method_with_strict_slash():
    request, response = app.test_client.get("/get/")
    assert response.text == 'I am get method'

def test_get_method_not_found():
    request, response = app.test_client.get("/nonexistent")
    assert response.status == 404

def test_get_method_with_query_params():
    request, response = app.test_client.get("/get?param=value")
    assert response.text == 'I am get method'  # Assuming query params do not affect the response

def test_get_method_with_invalid_method():
    request, response = app.test_client.post("/get")
    assert response.status == 405  # Method Not Allowed
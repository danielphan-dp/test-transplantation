import pytest
from sanic import Sanic
from sanic.response import text

app = Sanic("test_app")

@app.get("/")
def get(request):
    return text('I am get method')

def test_get_method_returns_correct_response():
    request, response = app.test_client.get("/")
    assert response.status == 200
    assert response.text == 'I am get method'

def test_get_method_with_invalid_route():
    request, response = app.test_client.get("/invalid")
    assert response.status == 404

def test_get_method_with_query_parameters():
    request, response = app.test_client.get("/?param=value")
    assert response.status == 200
    assert response.text == 'I am get method'

def test_get_method_with_headers():
    request, response = app.test_client.get("/", headers={"Custom-Header": "value"})
    assert response.status == 200
    assert response.text == 'I am get method'
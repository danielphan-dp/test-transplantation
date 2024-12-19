import json
from sanic import Sanic
from sanic.response import text
import pytest

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

@app.get("/")
async def get_handler(request):
    return text("I am get method")

def test_get_method(app):
    request, response = app.test_client.get("/")
    assert response.text == "I am get method"

def test_get_method_with_invalid_route(app):
    request, response = app.test_client.get("/invalid")
    assert response.status == 404

def test_get_method_with_query_params(app):
    request, response = app.test_client.get("/?param=test")
    assert response.text == "I am get method"  # Assuming the handler does not change based on query params

def test_get_method_with_headers(app):
    headers = {"Custom-Header": "value"}
    request, response = app.test_client.get("/", headers=headers)
    assert response.text == "I am get method"  # Assuming the handler does not change based on headers

def test_get_method_empty_response(app):
    @app.get("/empty")
    async def empty_handler(request):
        return text("")
    
    request, response = app.test_client.get("/empty")
    assert response.text == ""
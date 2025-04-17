import asyncio
import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_get_method(app):
    @app.get("/get")
    async def handler(request):
        return text("I am get method")

    request, response = app.test_client.get("/get")
    assert response.text == "I am get method"
    assert response.status == 200

def test_get_method_with_invalid_route(app):
    request, response = app.test_client.get("/invalid")
    assert response.status == 404
    assert "Requested URL /invalid not found" in response.text

def test_get_method_with_headers(app):
    @app.get("/get-with-headers")
    async def handler(request):
        return text("I am get method with headers")

    headers = {"Custom-Header": "value"}
    request, response = app.test_client.get("/get-with-headers", headers=headers)
    assert response.text == "I am get method with headers"
    assert response.status == 200

def test_get_method_with_query_params(app):
    @app.get("/get-with-query")
    async def handler(request):
        name = request.args.get("name", "World")
        return text(f"I am get method, hello {name}")

    request, response = app.test_client.get("/get-with-query?name=Test")
    assert response.text == "I am get method, hello Test"
    assert response.status == 200

def test_get_method_without_query_params(app):
    @app.get("/get-with-query")
    async def handler(request):
        name = request.args.get("name", "World")
        return text(f"I am get method, hello {name}")

    request, response = app.test_client.get("/get-with-query")
    assert response.text == "I am get method, hello World"
    assert response.status == 200
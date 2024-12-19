import asyncio
import pytest
from sanic import Sanic
from sanic.blueprints import Blueprint
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_get_method(app):
    @app.get("/get")
    async def get(request):
        return text("I am get method")

    request, response = app.test_client.get("/get")
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_not_found(app):
    request, response = app.test_client.get("/non_existent")
    assert response.status == 404
    assert "Requested URL /non_existent not found" in response.text

def test_get_method_with_query_params(app):
    @app.get("/get")
    async def get(request):
        return text(f"Query param: {request.args.get('param', 'not provided')}")

    request, response = app.test_client.get("/get?param=test")
    assert response.status == 200
    assert response.text == "Query param: test"

def test_get_method_with_headers(app):
    @app.get("/get")
    async def get(request):
        return text(f"Header value: {request.headers.get('X-Custom-Header', 'not provided')}")

    request, response = app.test_client.get("/get", headers={"X-Custom-Header": "value"})
    assert response.status == 200
    assert response.text == "Header value: value"

def test_get_method_empty_response(app):
    @app.get("/empty")
    async def empty(request):
        return text("")

    request, response = app.test_client.get("/empty")
    assert response.status == 200
    assert response.text == ""
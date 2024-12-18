import asyncio
import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.get("/")
    async def handler(request):
        return text("I am get method")

    return app

@pytest.mark.asyncio
async def test_get_method_response(app):
    request, response = await app.test_client.get("/")
    assert response.status == 200
    assert response.text == "I am get method"

@pytest.mark.asyncio
async def test_get_method_invalid_route(app):
    request, response = await app.test_client.get("/invalid")
    assert response.status == 404
    assert "Requested URL /invalid not found" in response.text

@pytest.mark.asyncio
async def test_get_method_with_query_param(app):
    @app.get("/greet")
    async def greet(request):
        name = request.args.get("name", "World")
        return text(f"Hello, {name}!")

    request, response = await app.test_client.get("/greet?name=Alice")
    assert response.status == 200
    assert response.text == "Hello, Alice!"

@pytest.mark.asyncio
async def test_get_method_with_empty_query_param(app):
    @app.get("/greet")
    async def greet(request):
        name = request.args.get("name", "World")
        return text(f"Hello, {name}!")

    request, response = await app.test_client.get("/greet?name=")
    assert response.status == 200
    assert response.text == "Hello, !"  # Edge case with empty query param

@pytest.mark.asyncio
async def test_get_method_with_large_query_param(app):
    @app.get("/greet")
    async def greet(request):
        name = request.args.get("name", "World")
        return text(f"Hello, {name}!")

    large_name = "A" * 1000
    request, response = await app.test_client.get(f"/greet?name={large_name}")
    assert response.status == 200
    assert response.text == f"Hello, {large_name}!"  # Edge case with large query param
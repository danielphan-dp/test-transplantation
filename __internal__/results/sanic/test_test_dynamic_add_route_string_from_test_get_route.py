import asyncio
import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_get_method(app):
    @app.get("/")
    async def handler(request):
        return text("I am get method")

    request, response = app.test_client.get("/")
    
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_with_invalid_route(app):
    request, response = app.test_client.get("/invalid")
    
    assert response.status == 404
    assert "Requested URL /invalid not found" in response.text

def test_get_method_with_middleware(app):
    results = []

    @app.middleware
    async def middleware(request):
        results.append(request)

    @app.get("/")
    async def handler(request):
        return text("I am get method")

    request, response = app.test_client.get("/")
    
    assert response.text == "I am get method"
    assert len(results) == 1
    assert results[0] is request

def test_get_method_with_query_params(app):
    @app.get("/greet")
    async def handler(request):
        name = request.args.get("name", "World")
        return text(f"Hello, {name}!")

    request, response = app.test_client.get("/greet?name=Alice")
    
    assert response.text == "Hello, Alice!"
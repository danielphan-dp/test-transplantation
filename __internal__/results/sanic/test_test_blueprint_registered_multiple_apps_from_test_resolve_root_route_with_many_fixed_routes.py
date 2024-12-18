import asyncio
import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_get_method_response(app):
    @app.get("/")
    async def handler(request):
        return text("I am get method")

    request, response = app.test_client.get("/")
    assert response.text == "I am get method"

def test_get_method_with_different_path(app):
    @app.get("/another")
    async def handler(request):
        return text("I am get method at another path")

    request, response = app.test_client.get("/another")
    assert response.text == "I am get method at another path"

def test_get_method_with_query_params(app):
    @app.get("/query")
    async def handler(request):
        return text(f"Query param: {request.args.get('param')}")

    request, response = app.test_client.get("/query?param=test")
    assert response.text == "Query param: test"

def test_get_method_not_found(app):
    request, response = app.test_client.get("/nonexistent")
    assert response.status == 404
    assert "Requested URL /nonexistent not found" in response.text

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
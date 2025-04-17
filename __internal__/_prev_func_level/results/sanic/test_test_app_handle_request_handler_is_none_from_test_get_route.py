import asyncio
import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

@pytest.mark.asyncio
async def test_get_method(app):
    @app.get("/get")
    def get_handler(request):
        return text("I am get method")

    request, response = await app.test_client.get("/get")
    assert response.status == 200
    assert response.text == "I am get method"

@pytest.mark.asyncio
async def test_get_method_not_found(app):
    request, response = await app.test_client.get("/nonexistent")
    assert response.status == 404
    assert "Requested URL /nonexistent not found" in response.text

@pytest.mark.asyncio
async def test_get_method_with_middleware(app):
    results = []

    @app.middleware
    async def middleware(request):
        results.append(request)

    @app.get("/middleware")
    def get_handler(request):
        return text("I am get method with middleware")

    request, response = await app.test_client.get("/middleware")
    assert response.text == "I am get method with middleware"
    assert len(results) == 1
    assert results[0] is request

@pytest.mark.asyncio
async def test_get_method_with_query_params(app):
    @app.get("/query")
    def get_handler(request):
        param = request.args.get("param", "default")
        return text(f"Query param is {param}")

    request, response = await app.test_client.get("/query?param=test")
    assert response.text == "Query param is test"

    request, response = await app.test_client.get("/query")
    assert response.text == "Query param is default"
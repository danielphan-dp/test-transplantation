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
    @app.get("/")
    async def handler(request):
        return text("I am get method")

    request, response = await app.test_client.get("/")
    assert response.status == 200
    assert response.text == "I am get method"

@pytest.mark.asyncio
async def test_get_method_with_different_route(app):
    @app.get("/different")
    async def handler(request):
        return text("I am get method on a different route")

    request, response = await app.test_client.get("/different")
    assert response.status == 200
    assert response.text == "I am get method on a different route"

@pytest.mark.asyncio
async def test_get_method_not_found(app):
    request, response = await app.test_client.get("/nonexistent")
    assert response.status == 404

@pytest.mark.asyncio
async def test_get_method_with_query_params(app):
    @app.get("/query")
    async def handler(request):
        param = request.args.get("param", "default")
        return text(f"Query param is {param}")

    request, response = await app.test_client.get("/query?param=test")
    assert response.status == 200
    assert response.text == "Query param is test"
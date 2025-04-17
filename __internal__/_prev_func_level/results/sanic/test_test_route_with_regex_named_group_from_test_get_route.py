import asyncio
import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.get("/get")
    async def get_handler(request):
        return text("I am get method")

    return app

@pytest.mark.asyncio
async def test_get_method(app):
    request, response = await app.test_client.get("/get")
    assert response.status == 200
    assert response.text == "I am get method"

@pytest.mark.asyncio
async def test_get_method_not_found(app):
    request, response = await app.test_client.get("/nonexistent")
    assert response.status == 404
    assert "Requested URL /nonexistent not found" in response.text

@pytest.mark.asyncio
async def test_get_method_with_query_param(app):
    request, response = await app.test_client.get("/get?param=value")
    assert response.status == 200
    assert response.text == "I am get method"  # No change in response for query params

@pytest.mark.asyncio
async def test_get_method_with_invalid_method(app):
    request, response = await app.test_client.post("/get")
    assert response.status == 405
    assert "Method POST not allowed for URL /get" in response.text
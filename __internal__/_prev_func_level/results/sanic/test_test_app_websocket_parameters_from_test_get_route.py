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
    def get_method(request):
        return text("I am get method")

    request, response = await app.test_client.get("/")
    assert response.status == 200
    assert response.text == "I am get method"

@pytest.mark.asyncio
async def test_get_method_with_invalid_route(app):
    request, response = await app.test_client.get("/invalid")
    assert response.status == 404
    assert "Requested URL /invalid not found" in response.text

@pytest.mark.asyncio
async def test_get_method_with_custom_header(app):
    @app.get("/")
    def get_method(request):
        return text("I am get method", headers={"X-Custom-Header": "value"})

    request, response = await app.test_client.get("/")
    assert response.status == 200
    assert response.headers["X-Custom-Header"] == "value"
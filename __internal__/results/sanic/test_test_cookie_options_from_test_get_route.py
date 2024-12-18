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
async def test_get_method(app):
    request, response = await app.test_client.get("/")
    assert response.status == 200
    assert await response.text() == "I am get method"

@pytest.mark.asyncio
async def test_get_method_with_invalid_route(app):
    request, response = await app.test_client.get("/invalid")
    assert response.status == 404
    assert "Requested URL /invalid not found" in await response.text()

@pytest.mark.asyncio
async def test_get_method_with_custom_header(app):
    @app.get("/")
    async def handler(request):
        response = text("I am get method")
        response.headers["X-Custom-Header"] = "CustomValue"
        return response

    request, response = await app.test_client.get("/")
    assert response.headers["X-Custom-Header"] == "CustomValue"
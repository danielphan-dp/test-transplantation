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
async def test_get_method(app):
    request, response = await app.test_client.get("/")
    assert response.status == 200
    assert await response.text() == "I am get method"

@pytest.mark.asyncio
async def test_get_method_not_found(app):
    request, response = await app.test_client.get("/nonexistent")
    assert response.status == 404

@pytest.mark.asyncio
async def test_get_method_with_delay(app):
    @app.get("/delayed")
    async def delayed_handler(request):
        await asyncio.sleep(0.1)
        return text("I am delayed get method")

    request, response = await app.test_client.get("/delayed")
    assert response.status == 200
    assert await response.text() == "I am delayed get method"
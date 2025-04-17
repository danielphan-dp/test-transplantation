import asyncio
import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.get("/")
    async def get_method(request):
        return text("I am get method")

    return app

@pytest.mark.asyncio
async def test_get_method_success(app):
    request, response = await app.test_client.get("/")
    assert response.status == 200
    assert response.text == "I am get method"

@pytest.mark.asyncio
async def test_get_method_not_found(app):
    request, response = await app.test_client.get("/nonexistent")
    assert response.status == 404
    assert "Requested URL /nonexistent not found" in response.text

@pytest.mark.asyncio
async def test_get_method_with_exception(app):
    @app.get("/error")
    async def error_method(request):
        raise Exception("Test Exception")

    event = asyncio.Event()

    @app.report_exception
    async def catch_exception(app: Sanic, exception: Exception):
        event.set()

    await app.test_client.get("/error")
    assert event.is_set()
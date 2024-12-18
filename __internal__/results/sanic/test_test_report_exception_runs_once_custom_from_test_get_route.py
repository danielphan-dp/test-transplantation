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
async def test_get_method_status(app):
    request, response = await app.test_client.get("/")
    assert response.status == 200

@pytest.mark.asyncio
async def test_get_method_response(app):
    request, response = await app.test_client.get("/")
    assert response.text == "I am get method"

@pytest.mark.asyncio
async def test_get_method_invalid_route(app):
    request, response = await app.test_client.get("/invalid")
    assert response.status == 404
    assert "Requested URL /invalid not found" in response.text

@pytest.mark.asyncio
async def test_get_method_with_custom_header(app):
    request, response = await app.test_client.get("/", headers={"Custom-Header": "value"})
    assert response.status == 200
    assert response.headers.get("Custom-Header") is None  # No custom header in response

@pytest.mark.asyncio
async def test_get_method_empty_body(app):
    request, response = await app.test_client.get("/")
    assert response.body == b"I am get method"  # Check the raw body response

import pytest
from sanic import Sanic, Request
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.get("/")
    async def get_method(request: Request):
        return text("I am get method")

    return app

@pytest.mark.asyncio
async def test_get_method(app):
    request, response = await app.test_client.get("/")
    assert response.status == 200
    assert response.text == "I am get method"
    assert response.headers["Content-Type"] == "text/plain; charset=utf-8"

@pytest.mark.asyncio
async def test_get_method_with_custom_header(app):
    request, response = await app.test_client.get("/", headers={"X-Custom-Header": "value"})
    assert response.status == 200
    assert response.text == "I am get method"
    assert response.headers["X-Custom-Header"] == "value"

@pytest.mark.asyncio
async def test_get_method_not_found(app):
    request, response = await app.test_client.get("/nonexistent")
    assert response.status == 404
    assert "Requested URL /nonexistent not found" in response.text

@pytest.mark.asyncio
async def test_get_method_with_query_param(app):
    request, response = await app.test_client.get("/?param=value")
    assert response.status == 200
    assert response.text == "I am get method"
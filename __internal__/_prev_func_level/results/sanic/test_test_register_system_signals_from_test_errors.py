import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.get("/get_method")
    async def get_method(request):
        return text("I am get method")

    return app

@pytest.mark.asyncio
async def test_get_method(app):
    request, response = await app.test_client.get("/get_method")
    assert response.status == 200
    assert response.text == "I am get method"
    assert response.headers.get("content-type") == "text/plain; charset=utf-8"

@pytest.mark.asyncio
async def test_get_method_not_found(app):
    request, response = await app.test_client.get("/non_existent_route")
    assert response.status == 404
    assert "Requested URL /non_existent_route not found" in response.text

@pytest.mark.asyncio
async def test_get_method_with_invalid_method(app):
    request, response = await app.test_client.post("/get_method")
    assert response.status == 405
    assert "Method POST not allowed for URL /get_method" in response.text

@pytest.mark.asyncio
async def test_get_method_with_custom_header(app):
    request, response = await app.test_client.get("/get_method", headers={"x-Custom-Header": "Test"})
    assert response.status == 200
    assert response.headers.get("x-Custom-Header") is None  # No custom header in response

@pytest.mark.asyncio
async def test_get_method_empty_response(app):
    @app.get("/empty_response")
    async def empty_response(request):
        return text("")

    request, response = await app.test_client.get("/empty_response")
    assert response.status == 200
    assert response.text == ""
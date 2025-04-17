import pytest
from sanic import Sanic
from sanic.text import text

@pytest.mark.asyncio
async def test_get_method(app: Sanic):
    @app.get("/test")
    async def get_method(request):
        return text("I am get method")

    request, response = await app.test_client.get("/test")
    assert response.status == 200
    assert response.text == "I am get method"

@pytest.mark.asyncio
async def test_get_method_with_query_param(app: Sanic):
    @app.get("/test")
    async def get_method(request):
        param = request.args.get("param", "default")
        return text(f"I am get method with param: {param}")

    request, response = await app.test_client.get("/test?param=value")
    assert response.status == 200
    assert response.text == "I am get method with param: value"

@pytest.mark.asyncio
async def test_get_method_not_found(app: Sanic):
    request, response = await app.test_client.get("/nonexistent")
    assert response.status == 404
    assert "Requested URL /nonexistent not found" in response.text

@pytest.mark.asyncio
async def test_get_method_invalid_method(app: Sanic):
    @app.get("/test")
    async def get_method(request):
        return text("I am get method")

    request, response = await app.test_client.post("/test")
    assert response.status == 405
    assert "Method POST not allowed for URL /test" in response.text
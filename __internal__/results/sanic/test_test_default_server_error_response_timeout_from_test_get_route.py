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
async def test_get_method_success(app):
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
    @app.get("/get_with_param")
    async def get_with_param(request):
        param = request.args.get("param", "default")
        return text(f"I am get method with param: {param}")

    request, response = await app.test_client.get("/get_with_param?param=test")
    assert response.status == 200
    assert response.text == "I am get method with param: test"
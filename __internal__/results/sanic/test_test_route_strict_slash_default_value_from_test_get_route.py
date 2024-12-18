import asyncio
import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_get_method")
    return app

@pytest.mark.asyncio
async def test_get_method(app):
    @app.get("/get")
    def handler(request):
        return text("I am get method")

    request, response = await app.test_client.get("/get")
    assert response.status == 200
    assert response.text == "I am get method"

@pytest.mark.asyncio
async def test_get_method_not_found(app):
    request, response = await app.test_client.get("/nonexistent")
    assert response.status == 404

@pytest.mark.asyncio
async def test_get_method_strict_slash(app):
    @app.get("/get")
    def handler(request):
        return text("I am get method")

    request, response = await app.test_client.get("/get/")
    assert response.status == 404

@pytest.mark.asyncio
async def test_get_method_with_query_param(app):
    @app.get("/get")
    def handler(request):
        return text(f"I am get method with param: {request.args.get('param')}")

    request, response = await app.test_client.get("/get?param=test")
    assert response.status == 200
    assert response.text == "I am get method with param: test"
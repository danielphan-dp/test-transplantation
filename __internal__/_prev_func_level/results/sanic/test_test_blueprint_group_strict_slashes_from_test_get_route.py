import asyncio
import pytest
from sanic import Sanic
from sanic.blueprints import Blueprint
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

@pytest.fixture
def test_client(app):
    return app.test_client

@pytest.mark.asyncio
async def test_get_method(app, test_client):
    @app.get("/get")
    async def get_method(request):
        return text("I am get method")

    request, response = await test_client.get("/get")
    assert response.status == 200
    assert response.text == "I am get method"

@pytest.mark.asyncio
async def test_get_method_not_found(app, test_client):
    request, response = await test_client.get("/nonexistent")
    assert response.status == 404

@pytest.mark.asyncio
async def test_get_method_with_query_param(app, test_client):
    @app.get("/get_with_param")
    async def get_with_param(request):
        param = request.args.get("param", "default")
        return text(f"Received param: {param}")

    request, response = await test_client.get("/get_with_param?param=test")
    assert response.status == 200
    assert response.text == "Received param: test"

@pytest.mark.asyncio
async def test_get_method_empty_query_param(app, test_client):
    @app.get("/get_with_param")
    async def get_with_param(request):
        param = request.args.get("param", "default")
        return text(f"Received param: {param}")

    request, response = await test_client.get("/get_with_param")
    assert response.status == 200
    assert response.text == "Received param: default"
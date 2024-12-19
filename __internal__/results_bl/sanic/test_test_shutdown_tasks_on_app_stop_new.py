import asyncio
from unittest.mock import Mock, AsyncMock
import pytest
from sanic import Sanic
from sanic.response import text

class TestSanic(Sanic):
    pass

@pytest.fixture
def app():
    app = TestSanic("Test")
    return app

@pytest.mark.asyncio
async def test_get_method(app):
    @app.route("/get")
    async def handler(request):
        return text('I am get method')

    request, response = await app.test_client.get("/get")
    assert response.status == 200
    assert response.text == 'I am get method'

@pytest.mark.asyncio
async def test_get_method_not_found(app):
    @app.route("/get")
    async def handler(request):
        return text('I am get method')

    request, response = await app.test_client.get("/nonexistent")
    assert response.status == 404

@pytest.mark.asyncio
async def test_get_method_empty_request(app):
    @app.route("/get")
    async def handler(request):
        return text('I am get method')

    request, response = await app.test_client.get("/get", data={})
    assert response.status == 200
    assert response.text == 'I am get method'
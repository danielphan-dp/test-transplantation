import asyncio
import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")

    @app.put("/put")
    async def put(request):
        return text("I am put method")

    return app

@pytest.mark.asyncio
async def test_put_method(app):
    request, response = await app.asgi_client.put("/put")
    assert response.status == 200
    assert response.text == "I am put method"

@pytest.mark.asyncio
async def test_put_method_with_data(app):
    data = "Test data"
    request, response = await app.asgi_client.put("/put", data=data)
    assert response.status == 200
    assert response.text == "I am put method"

@pytest.mark.asyncio
async def test_put_method_empty_body(app):
    request, response = await app.asgi_client.put("/put", data="")
    assert response.status == 200
    assert response.text == "I am put method"

@pytest.mark.asyncio
async def test_put_method_invalid_route(app):
    request, response = await app.asgi_client.put("/invalid_route")
    assert response.status == 404

@pytest.mark.asyncio
async def test_put_method_with_large_data(app):
    large_data = "A" * 10000
    request, response = await app.asgi_client.put("/put", data=large_data)
    assert response.status == 200
    assert response.text == "I am put method"
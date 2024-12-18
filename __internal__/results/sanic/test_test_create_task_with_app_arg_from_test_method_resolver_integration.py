import asyncio
import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")

    @app.put("/put")
    async def put_method(request):
        return text("I am put method")

    return app

@pytest.mark.asyncio
async def test_put_method(app):
    request, response = await app.asgi_client.put("/put")
    assert response.status == 200
    assert response.text == "I am put method"

@pytest.mark.asyncio
async def test_put_method_with_data(app):
    request, response = await app.asgi_client.put("/put", json={"key": "value"})
    assert response.status == 200
    assert response.text == "I am put method"

@pytest.mark.asyncio
async def test_put_method_invalid_route(app):
    request, response = await app.asgi_client.put("/invalid")
    assert response.status == 404

@pytest.mark.asyncio
async def test_put_method_empty_body(app):
    request, response = await app.asgi_client.put("/put", data="")
    assert response.status == 200
    assert response.text == "I am put method"
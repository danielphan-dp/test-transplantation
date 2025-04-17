import pytest
from aiohttp import web
from aiohttp.test_utils import AiohttpClient

@pytest.fixture
async def app():
    app = web.Application()
    app[my_value] = "test_value"
    app.router.add_get("/test/{name}", make_handler("test_app"))
    return app

@pytest.mark.asyncio
async def test_handler_returns_ok(aiohttp_client: AiohttpClient, app):
    client = await aiohttp_client(app)
    response = await client.get("/test/John")
    assert response.status == 200
    text = await response.text()
    assert text == "Ok"

@pytest.mark.asyncio
async def test_handler_includes_app_value(aiohttp_client: AiohttpClient, app):
    client = await aiohttp_client(app)
    response = await client.get("/test/John")
    assert response.status == 200
    assert 'test_app: test_value' in values

@pytest.mark.asyncio
async def test_handler_with_different_name(aiohttp_client: AiohttpClient, app):
    client = await aiohttp_client(app)
    response = await client.get("/test/Jane")
    assert response.status == 200
    assert 'test_app: test_value' in values

@pytest.mark.asyncio
async def test_handler_invalid_route(aiohttp_client: AiohttpClient, app):
    client = await aiohttp_client(app)
    response = await client.get("/invalid_route")
    assert response.status == 404

@pytest.mark.asyncio
async def test_handler_empty_name(aiohttp_client: AiohttpClient, app):
    client = await aiohttp_client(app)
    response = await client.get("/test/")
    assert response.status == 404
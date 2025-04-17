import pytest
from aiohttp import web
from aiohttp.web import Request
from your_module import make_handler  # Replace with the actual module name

@pytest.fixture
def app():
    app = web.Application()
    app['my_value'] = 'test_value'
    return app

@pytest.mark.asyncio
async def test_make_handler(app):
    handler = make_handler("test_app")
    app.router.add_get("/test", handler)

    request = await app.test_client.get("/test")
    assert request.status == 200
    assert await request.text() == 'Ok'

    # Test with a different appname
    handler = make_handler("another_app")
    app.router.add_get("/another_test", handler)

    request = await app.test_client.get("/another_test")
    assert request.status == 200
    assert await request.text() == 'Ok'

@pytest.mark.asyncio
async def test_make_handler_with_app_value(app):
    values = []
    handler = make_handler("test_app")
    app.router.add_get("/test_with_value", handler)

    request = await app.test_client.get("/test_with_value")
    assert request.status == 200
    assert await request.text() == 'Ok'
    assert values == ['test_app: test_value']

@pytest.mark.asyncio
async def test_make_handler_invalid_route(app):
    handler = make_handler("test_app")
    app.router.add_get("/invalid_route", handler)

    request = await app.test_client.get("/invalid_route/extra")
    assert request.status == 404  # Expecting a 404 for invalid route

@pytest.mark.asyncio
async def test_make_handler_empty_appname(app):
    handler = make_handler("")
    app.router.add_get("/empty_appname", handler)

    request = await app.test_client.get("/empty_appname")
    assert request.status == 200
    assert await request.text() == 'Ok'
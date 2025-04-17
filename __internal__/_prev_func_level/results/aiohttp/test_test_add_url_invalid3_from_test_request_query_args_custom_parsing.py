import pytest
from aiohttp import web
from aiohttp.web import Request
from your_module import make_handler  # Replace with the actual module name

@pytest.fixture
def app():
    app = web.Application()
    return app

@pytest.mark.asyncio
async def test_make_handler_valid(app):
    appname = "test_app"
    handler = make_handler(appname)
    app.router.add_get("/", handler)

    request = await app.test_client.get("/")
    assert request.status == 200
    assert await request.text() == "Ok"

@pytest.mark.asyncio
async def test_make_handler_with_app_value(app):
    app['my_value'] = "test_value"
    appname = "test_app"
    values = []
    handler = make_handler(appname)
    app.router.add_get("/", handler)

    request = await app.test_client.get("/")
    assert request.status == 200
    assert await request.text() == "Ok"
    assert values == [f'{appname}: test_value']

@pytest.mark.asyncio
async def test_make_handler_invalid_app_value(app):
    appname = "test_app"
    handler = make_handler(appname)
    app.router.add_get("/", handler)

    app['my_value'] = None  # Simulating an invalid value
    request = await app.test_client.get("/")
    assert request.status == 200
    assert await request.text() == "Ok"

@pytest.mark.asyncio
async def test_make_handler_no_app_value(app):
    appname = "test_app"
    handler = make_handler(appname)
    app.router.add_get("/", handler)

    request = await app.test_client.get("/")
    assert request.status == 200
    assert await request.text() == "Ok"
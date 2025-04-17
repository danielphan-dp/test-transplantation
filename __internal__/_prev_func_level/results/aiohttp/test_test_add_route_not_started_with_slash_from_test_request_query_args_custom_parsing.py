import pytest
from aiohttp import web
from aiohttp.web import Request

@pytest.fixture
def app():
    return web.Application()

@pytest.fixture
def router(app):
    return app.router

@pytest.mark.asyncio
async def test_make_handler_with_valid_appname(router):
    values = []
    appname = "test_app"
    handler = make_handler(appname)
    router.add_route("GET", "/test", handler)

    request = await router["/test"].get()
    response = await handler(request)

    assert response.status == 200
    assert await response.text() == 'Ok'
    assert values == [f'{appname}: {request.app[my_value]}']

@pytest.mark.asyncio
async def test_make_handler_with_invalid_appname(router):
    values = []
    appname = ""
    handler = make_handler(appname)
    router.add_route("GET", "/test", handler)

    request = await router["/test"].get()
    response = await handler(request)

    assert response.status == 200
    assert await response.text() == 'Ok'
    assert values == [f'{appname}: {request.app[my_value]}']

@pytest.mark.asyncio
async def test_make_handler_with_no_appname(router):
    values = []
    appname = None
    handler = make_handler(appname)
    router.add_route("GET", "/test", handler)

    request = await router["/test"].get()
    response = await handler(request)

    assert response.status == 200
    assert await response.text() == 'Ok'
    assert values == [f'{appname}: {request.app[my_value]}']
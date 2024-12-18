import pytest
from aiohttp import web
from aiohttp.web import Request
from aiohttp.test_utils import make_mocked_request
from your_module import make_handler  # Replace with the actual module name

@pytest.fixture
def router():
    return web.UrlDispatcher()

@pytest.mark.asyncio
async def test_make_handler_returns_ok(router):
    appname = "test_app"
    handler = make_handler(appname)
    router.add_route("GET", "/test", handler)

    request = make_mocked_request("GET", "/test", app=web.Application())
    response = await handler(request)

    assert response.status == 200
    assert await response.text() == 'Ok'

@pytest.mark.asyncio
async def test_make_handler_includes_appname(router):
    appname = "test_app"
    my_value = "my_value"
    router.add_route("GET", "/test", make_handler(appname))

    request = make_mocked_request("GET", "/test", app=web.Application())
    request.app[my_value] = "value_from_app"

    response = await make_handler(appname)(request)

    assert response.status == 200
    assert await response.text() == 'Ok'
    assert request.app[my_value] == "value_from_app"

@pytest.mark.asyncio
async def test_make_handler_with_different_appname(router):
    appname = "another_app"
    my_value = "my_value"
    router.add_route("GET", "/test", make_handler(appname))

    request = make_mocked_request("GET", "/test", app=web.Application())
    request.app[my_value] = "different_value"

    response = await make_handler(appname)(request)

    assert response.status == 200
    assert await response.text() == 'Ok'
    assert request.app[my_value] == "different_value"
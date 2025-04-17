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
    assert response.text == 'Ok'

@pytest.mark.asyncio
async def test_make_handler_inserts_appname(router):
    appname = "test_app"
    my_value = "my_value"
    values = []
    handler = make_handler(appname)
    router.add_route("GET", "/test", handler)

    request = make_mocked_request("GET", "/test", app=web.Application())
    request.app[my_value] = "value_1"
    await handler(request)

    assert f'{appname}: value_1' in values

@pytest.mark.asyncio
async def test_make_handler_with_different_appname(router):
    appname = "another_app"
    my_value = "my_value"
    values = []
    handler = make_handler(appname)
    router.add_route("GET", "/test", handler)

    request = make_mocked_request("GET", "/test", app=web.Application())
    request.app[my_value] = "value_2"
    await handler(request)

    assert f'{appname}: value_2' in values

@pytest.mark.asyncio
async def test_make_handler_with_missing_value(router):
    appname = "test_app"
    handler = make_handler(appname)
    router.add_route("GET", "/test", handler)

    request = make_mocked_request("GET", "/test", app=web.Application())
    request.app.pop("my_value", None)
    response = await handler(request)

    assert response.status == 200
    assert response.text == 'Ok'  # Ensure it still returns 'Ok' even if my_value is missing

@pytest.mark.asyncio
async def test_make_handler_invalid_method(router):
    appname = "test_app"
    handler = make_handler(appname)
    router.add_route("POST", "/test", handler)

    request = make_mocked_request("GET", "/test", app=web.Application())
    response = await handler(request)

    assert response.status == 405  # Method Not Allowed
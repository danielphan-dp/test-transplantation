import pytest
from aiohttp import web
from aiohttp.web import Request, Response
from aiohttp.test_utils import make_mocked_request
from your_module import make_handler  # Replace with the actual module name

@pytest.fixture
def router():
    return web.UrlDispatcher()

@pytest.mark.asyncio
async def test_make_handler_returns_ok(router):
    appname = "test_app"
    handler = make_handler(appname)
    router.add_route("GET", "/", handler)

    request = make_mocked_request("GET", "/")
    response = await handler(request)

    assert response.status == 200
    assert response.text == 'Ok'

@pytest.mark.asyncio
async def test_make_handler_inserts_appname(router):
    appname = "test_app"
    my_value = "my_value"
    values = []
    handler = make_handler(appname)
    router.add_route("GET", "/", handler)

    request = make_mocked_request("GET", "/", app={my_value: "value1"})
    await handler(request)

    assert values == [f'{appname}: value1']

@pytest.mark.asyncio
async def test_make_handler_with_different_appname(router):
    appname = "another_app"
    my_value = "my_value"
    values = []
    handler = make_handler(appname)
    router.add_route("GET", "/", handler)

    request = make_mocked_request("GET", "/", app={my_value: "value2"})
    await handler(request)

    assert values == [f'{appname}: value2']

@pytest.mark.asyncio
async def test_make_handler_with_no_app_value(router):
    appname = "test_app"
    my_value = "my_value"
    values = []
    handler = make_handler(appname)
    router.add_route("GET", "/", handler)

    request = make_mocked_request("GET", "/", app={})
    await handler(request)

    assert values == [f'{appname}: None']  # Assuming None is the default when my_value is not present

@pytest.mark.asyncio
async def test_make_handler_invalid_method(router):
    appname = "test_app"
    handler = make_handler(appname)
    router.add_route("POST", "/", handler)

    request = make_mocked_request("GET", "/")
    with pytest.raises(web.HTTPMethodNotAllowed):
        await handler(request)
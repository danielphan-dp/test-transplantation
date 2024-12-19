import pytest
from aiohttp import web
from your_module import make_handler  # Replace 'your_module' with the actual module name

@pytest.fixture
def router():
    return web.UrlDispatcher()

@pytest.mark.asyncio
async def test_make_handler_valid_request(router):
    appname = "test_app"
    my_value = "test_value"
    values = []
    handler = make_handler(appname)
    router.add_route("GET", "/valid_path", handler)
    request = web.Request(web.Request, "GET", "/valid_path", app={my_value: "some_value"})
    response = await handler(request)
    assert response.text == 'Ok'
    assert values == [f'{appname}: some_value']

@pytest.mark.asyncio
async def test_make_handler_invalid_request(router):
    appname = "test_app"
    handler = make_handler(appname)
    request = web.Request(web.Request, "GET", "/invalid_path", app={})
    response = await handler(request)
    assert response.text == 'Ok'
    assert values == [f'{appname}: None']

@pytest.mark.asyncio
async def test_make_handler_no_app_value(router):
    appname = "test_app"
    my_value = "test_value"
    values = []
    handler = make_handler(appname)
    request = web.Request(web.Request, "GET", "/valid_path", app={my_value: None})
    response = await handler(request)
    assert response.text == 'Ok'
    assert values == [f'{appname}: None']
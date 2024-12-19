import pytest
from aiohttp import web
from aiohttp.test_utils import make_mocked_request

@pytest.fixture
def router():
    return web.UrlDispatcher()

@pytest.mark.asyncio
async def test_make_handler_with_valid_appname(router):
    appname = "test_app"
    my_value = "value_key"
    router[my_value] = "test_value"
    handler = make_handler(appname)
    request = make_mocked_request("GET", "/handler/to/path", app=router)
    response = await handler(request)
    assert response.text == 'Ok'
    assert f'{appname}: test_value' in values

@pytest.mark.asyncio
async def test_make_handler_with_empty_appname(router):
    appname = ""
    my_value = "value_key"
    router[my_value] = "test_value"
    handler = make_handler(appname)
    request = make_mocked_request("GET", "/handler/to/path", app=router)
    response = await handler(request)
    assert response.text == 'Ok'
    assert f'{appname}: test_value' in values

@pytest.mark.asyncio
async def test_make_handler_with_nonexistent_key(router):
    appname = "test_app"
    my_value = "nonexistent_key"
    handler = make_handler(appname)
    request = make_mocked_request("GET", "/handler/to/path", app=router)
    response = await handler(request)
    assert response.text == 'Ok'
    assert f'{appname}: None' in values

@pytest.mark.asyncio
async def test_make_handler_with_uncommon_http_methods(router):
    uncommon_http_methods = {
        "PROPFIND",
        "PROPPATCH",
        "COPY",
        "LOCK",
        "UNLOCK",
        "MOVE",
        "SUBSCRIBE",
        "UNSUBSCRIBE",
        "NOTIFY",
    }
    appname = "test_app"
    my_value = "value_key"
    router[my_value] = "test_value"
    for method in uncommon_http_methods:
        handler = make_handler(appname)
        request = make_mocked_request(method, "/handler/to/path", app=router)
        response = await handler(request)
        assert response.text == 'Ok'
        assert f'{appname}: test_value' in values
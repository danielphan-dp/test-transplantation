import asyncio
import pytest
from aiohttp import web
from aiohttp.web_urldispatcher import make_handler

@pytest.fixture
def router():
    return web.UrlDispatcher()

@pytest.mark.asyncio
async def test_make_handler_valid_request(router):
    appname = "test_app"
    my_value = "value_key"
    router[my_value] = "test_value"
    handler = make_handler(appname)
    request = web.Request(
        method='GET',
        path='/get/test',
        app=web.Application(router=router)
    )
    response = await handler(request)
    assert response.text == 'Ok'
    assert f'{appname}: test_value' in values

@pytest.mark.asyncio
async def test_make_handler_no_value_key(router):
    appname = "test_app"
    my_value = "value_key"
    handler = make_handler(appname)
    request = web.Request(
        method='GET',
        path='/get/test',
        app=web.Application(router=router)
    )
    response = await handler(request)
    assert response.text == 'Ok'
    assert f'{appname}: None' in values

@pytest.mark.asyncio
async def test_make_handler_empty_appname(router):
    appname = ""
    my_value = "value_key"
    router[my_value] = "test_value"
    handler = make_handler(appname)
    request = web.Request(
        method='GET',
        path='/get/test',
        app=web.Application(router=router)
    )
    response = await handler(request)
    assert response.text == 'Ok'
    assert f'{appname}: test_value' in values

@pytest.mark.asyncio
async def test_make_handler_invalid_request_method(router):
    appname = "test_app"
    my_value = "value_key"
    router[my_value] = "test_value"
    handler = make_handler(appname)
    request = web.Request(
        method='POST',
        path='/get/test',
        app=web.Application(router=router)
    )
    with pytest.raises(web.HTTPMethodNotAllowed):
        await handler(request)
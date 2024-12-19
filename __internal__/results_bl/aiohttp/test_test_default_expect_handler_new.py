import pytest
from aiohttp import web
from aiohttp.web_urldispatcher import make_handler

@pytest.fixture
def router():
    return web.UrlDispatcher()

@pytest.mark.asyncio
async def test_make_handler_valid_request(router):
    appname = "test_app"
    my_value = "test_value"
    router[my_value] = "value_from_app"
    handler = make_handler(appname)
    router.add_route("GET", "/", handler)
    
    request = web.Request(method='GET', path='/', app=router)
    response = await handler(request)
    
    assert response.text == 'Ok'
    assert f'{appname}: value_from_app' in values

@pytest.mark.asyncio
async def test_make_handler_no_value_in_app(router):
    appname = "test_app"
    my_value = "test_value"
    handler = make_handler(appname)
    router.add_route("GET", "/", handler)
    
    request = web.Request(method='GET', path='/', app=router)
    response = await handler(request)
    
    assert response.text == 'Ok'
    assert f'{appname}: None' in values

@pytest.mark.asyncio
async def test_make_handler_empty_appname(router):
    appname = ""
    my_value = "test_value"
    router[my_value] = "value_from_app"
    handler = make_handler(appname)
    router.add_route("GET", "/", handler)
    
    request = web.Request(method='GET', path='/', app=router)
    response = await handler(request)
    
    assert response.text == 'Ok'
    assert f'{appname}: value_from_app' in values

@pytest.mark.asyncio
async def test_make_handler_invalid_method(router):
    appname = "test_app"
    my_value = "test_value"
    router[my_value] = "value_from_app"
    handler = make_handler(appname)
    router.add_route("POST", "/", handler)
    
    request = web.Request(method='GET', path='/', app=router)
    with pytest.raises(web.HTTPMethodNotAllowed):
        await handler(request)
import pytest
from aiohttp import web
from aiohttp.web_urldispatcher import UrlDispatcher
from your_module import make_handler  # Adjust the import according to your module structure

@pytest.fixture
def router():
    return web.UrlDispatcher()

@pytest.mark.asyncio
async def test_make_handler_valid_request(router):
    appname = "test_app"
    my_value = "my_value"
    router.add_route("GET", "/test", make_handler(appname), name="test_route")
    request = web.Request(web.HTTPrequest, "GET", "/test", app=web.Application())
    request.app[my_value] = "test_value"
    
    handler = make_handler(appname)
    response = await handler(request)
    
    assert response.status == 200
    assert response.text == 'Ok'

@pytest.mark.asyncio
async def test_make_handler_missing_value(router):
    appname = "test_app"
    my_value = "my_value"
    router.add_route("GET", "/test", make_handler(appname), name="test_route")
    request = web.Request(web.HTTPrequest, "GET", "/test", app=web.Application())
    
    handler = make_handler(appname)
    response = await handler(request)
    
    assert response.status == 200
    assert response.text == 'Ok'

@pytest.mark.asyncio
async def test_make_handler_different_appname(router):
    appname = "another_app"
    my_value = "my_value"
    router.add_route("GET", "/test", make_handler(appname), name="test_route")
    request = web.Request(web.HTTPrequest, "GET", "/test", app=web.Application())
    request.app[my_value] = "another_value"
    
    handler = make_handler(appname)
    response = await handler(request)
    
    assert response.status == 200
    assert response.text == 'Ok'
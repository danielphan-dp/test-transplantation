import pytest
from aiohttp import web
from aiohttp.web import Request
from your_module import make_handler  # Adjust the import according to your module structure

@pytest.fixture
def router():
    return web.UrlDispatcher()

@pytest.mark.asyncio
async def test_make_handler_with_valid_appname(router):
    appname = "TestApp"
    handler = make_handler(appname)
    router.add_route("GET", "/test/", handler, name="test_route")
    
    request = Request(method='GET', path='/test/', app={'my_value': 'Hello'})
    response = await handler(request)
    
    assert response.status == 200
    assert await response.text() == 'Ok'

@pytest.mark.asyncio
async def test_make_handler_with_different_appname(router):
    appname = "AnotherApp"
    handler = make_handler(appname)
    router.add_route("GET", "/another_test/", handler, name="another_test_route")
    
    request = Request(method='GET', path='/another_test/', app={'my_value': 'World'})
    response = await handler(request)
    
    assert response.status == 200
    assert await response.text() == 'Ok'

@pytest.mark.asyncio
async def test_make_handler_with_missing_my_value(router):
    appname = "MissingValueApp"
    handler = make_handler(appname)
    router.add_route("GET", "/missing_value/", handler, name="missing_value_route")
    
    request = Request(method='GET', path='/missing_value/', app={})
    response = await handler(request)
    
    assert response.status == 200
    assert await response.text() == 'Ok'

@pytest.mark.asyncio
async def test_make_handler_with_invalid_request_method(router):
    appname = "InvalidMethodApp"
    handler = make_handler(appname)
    router.add_route("POST", "/invalid_method/", handler, name="invalid_method_route")
    
    request = Request(method='POST', path='/invalid_method/', app={'my_value': 'Test'})
    response = await handler(request)
    
    assert response.status == 200
    assert await response.text() == 'Ok'
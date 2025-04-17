import pytest
from aiohttp import web
from aiohttp.web import Request
from your_module import make_handler  # Replace with the actual module name

@pytest.fixture
def router():
    return web.UrlDispatcher()

@pytest.mark.asyncio
async def test_handler_response(router):
    appname = "test_app"
    handler = make_handler(appname)
    router.add_route("GET", "/test", handler, name="test_route")
    
    request = Request(method='GET', path='/test', app={'my_value': 'value'})
    response = await handler(request)
    
    assert response.status == 200
    assert await response.text() == 'Ok'

@pytest.mark.asyncio
async def test_handler_with_different_appname(router):
    appname = "another_app"
    handler = make_handler(appname)
    router.add_route("GET", "/another_test", handler, name="another_route")
    
    request = Request(method='GET', path='/another_test', app={'my_value': 'another_value'})
    response = await handler(request)
    
    assert response.status == 200
    assert await response.text() == 'Ok'

@pytest.mark.asyncio
async def test_handler_appname_in_values(router):
    appname = "test_app"
    values = []
    handler = make_handler(appname)
    router.add_route("GET", "/test_values", handler, name="test_values_route")
    
    request = Request(method='GET', path='/test_values', app={'my_value': 'value'})
    await handler(request)
    
    assert f'{appname}: value' in values

@pytest.mark.asyncio
async def test_handler_invalid_route(router):
    appname = "test_app"
    handler = make_handler(appname)
    router.add_route("GET", "/valid_route", handler, name="valid_route")
    
    request = Request(method='GET', path='/invalid_route', app={'my_value': 'value'})
    response = await handler(request)
    
    assert response.status == 404  # Assuming the handler should return 404 for invalid routes

@pytest.mark.asyncio
async def test_handler_no_app_value(router):
    appname = "test_app"
    handler = make_handler(appname)
    router.add_route("GET", "/no_value", handler, name="no_value_route")
    
    request = Request(method='GET', path='/no_value', app={})
    response = await handler(request)
    
    assert response.status == 200
    assert await response.text() == 'Ok'  # Check if it still responds correctly without 'my_value' in app
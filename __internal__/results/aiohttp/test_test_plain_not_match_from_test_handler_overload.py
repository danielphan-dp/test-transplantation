import pytest
from aiohttp import web
from aiohttp.web import Request
from aiohttp.test_utils import make_mocked_request
from your_module import make_handler  # Replace with the actual module name

@pytest.fixture
def router():
    return web.UrlDispatcher()

@pytest.mark.asyncio
async def test_make_handler_valid_request(router):
    appname = "test_app"
    my_value = "my_value"
    values = []
    handler = make_handler(appname)
    router.add_route("GET", "/test/path", handler, name="test_route")
    
    request = make_mocked_request("GET", "/test/path", app={my_value: "value"})
    response = await handler(request)
    
    assert response.status == 200
    assert await response.text() == 'Ok'
    assert values == [f'{appname}: value']

@pytest.mark.asyncio
async def test_make_handler_no_value(router):
    appname = "test_app"
    my_value = "my_value"
    values = []
    handler = make_handler(appname)
    router.add_route("GET", "/test/path", handler, name="test_route")
    
    request = make_mocked_request("GET", "/test/path", app={})
    response = await handler(request)
    
    assert response.status == 200
    assert await response.text() == 'Ok'
    assert values == [f'{appname}: None']

@pytest.mark.asyncio
async def test_make_handler_invalid_method(router):
    appname = "test_app"
    handler = make_handler(appname)
    router.add_route("POST", "/test/path", handler, name="test_route")
    
    request = make_mocked_request("GET", "/test/path")
    response = await handler(request)
    
    assert response.status == 200
    assert await response.text() == 'Ok'  # Ensure it still responds correctly

@pytest.mark.asyncio
async def test_make_handler_multiple_requests(router):
    appname = "test_app"
    my_value = "my_value"
    values = []
    handler = make_handler(appname)
    router.add_route("GET", "/test/path", handler, name="test_route")
    
    request1 = make_mocked_request("GET", "/test/path", app={my_value: "value1"})
    request2 = make_mocked_request("GET", "/test/path", app={my_value: "value2"})
    
    await handler(request1)
    await handler(request2)
    
    assert values == [f'{appname}: value1', f'{appname}: value2']
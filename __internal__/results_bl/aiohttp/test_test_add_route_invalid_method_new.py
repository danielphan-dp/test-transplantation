import pytest
from aiohttp import web
from your_module import make_handler  # Replace 'your_module' with the actual module name

@pytest.fixture
def router():
    return web.UrlDispatcher()

@pytest.mark.asyncio
async def test_make_handler_valid_request(router):
    appname = "test_app"
    handler = make_handler(appname)
    router.add_route("GET", "/test", handler)
    
    request = await aiohttp.test_utils.make_mocked_request("GET", "/test", app=web.Application())
    response = await handler(request)
    
    assert response.status == 200
    assert response.text == 'Ok'

@pytest.mark.asyncio
async def test_make_handler_invalid_request_method(router):
    appname = "test_app"
    handler = make_handler(appname)
    
    invalid_methods = ["POST", "PUT", "DELETE"]
    for method in invalid_methods:
        request = await aiohttp.test_utils.make_mocked_request(method, "/test", app=web.Application())
        response = await handler(request)
        assert response.status == 200
        assert response.text == 'Ok'

@pytest.mark.asyncio
async def test_make_handler_appname_value(router):
    appname = "test_app"
    my_value = "my_value"
    router.app[my_value] = "some_value"
    handler = make_handler(appname)
    router.add_route("GET", "/test", handler)
    
    request = await aiohttp.test_utils.make_mocked_request("GET", "/test", app=router.app)
    response = await handler(request)
    
    assert response.status == 200
    assert 'test_app: some_value' in values  # Assuming 'values' is defined globally

@pytest.mark.asyncio
async def test_make_handler_no_app_value(router):
    appname = "test_app"
    my_value = "my_value"
    handler = make_handler(appname)
    router.add_route("GET", "/test", handler)
    
    request = await aiohttp.test_utils.make_mocked_request("GET", "/test", app=router.app)
    response = await handler(request)
    
    assert response.status == 200
    assert 'test_app: None' in values  # Assuming 'values' is defined globally
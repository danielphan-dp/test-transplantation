import pytest
from aiohttp import web
from aiohttp.web_urldispatcher import UrlDispatcher
from your_module import make_handler  # Adjust the import according to your module structure

@pytest.fixture
def router():
    return UrlDispatcher()

@pytest.mark.asyncio
async def test_handler_response(router):
    appname = "test_app"
    handler = make_handler(appname)
    router.add_route("GET", "/test", handler, name="test_route")
    
    request = await aiohttp.test_utils.make_mocked_request("GET", "/test", app=web.Application())
    response = await handler(request)
    
    assert response.status == 200
    assert await response.text() == 'Ok'

@pytest.mark.asyncio
async def test_handler_with_different_appname(router):
    appname = "another_app"
    handler = make_handler(appname)
    router.add_route("GET", "/another_test", handler, name="another_route")
    
    request = await aiohttp.test_utils.make_mocked_request("GET", "/another_test", app=web.Application())
    response = await handler(request)
    
    assert response.status == 200
    assert await response.text() == 'Ok'

@pytest.mark.asyncio
async def test_handler_with_no_appname(router):
    appname = ""
    handler = make_handler(appname)
    router.add_route("GET", "/no_appname", handler, name="no_appname_route")
    
    request = await aiohttp.test_utils.make_mocked_request("GET", "/no_appname", app=web.Application())
    response = await handler(request)
    
    assert response.status == 200
    assert await response.text() == 'Ok'

@pytest.mark.asyncio
async def test_handler_with_invalid_request(router):
    appname = "test_app"
    handler = make_handler(appname)
    router.add_route("GET", "/invalid_request", handler, name="invalid_route")
    
    request = await aiohttp.test_utils.make_mocked_request("POST", "/invalid_request", app=web.Application())
    response = await handler(request)
    
    assert response.status == 405  # Method Not Allowed
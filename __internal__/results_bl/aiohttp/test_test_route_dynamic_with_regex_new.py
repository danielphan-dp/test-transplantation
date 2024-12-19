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
    router.add_route("GET", r"/{one}/{two:.+}", handler)

    request = await aiohttp.test_utils.make_mocked_request("GET", "/1/2", app=web.Application())
    response = await handler(request)
    
    assert response.status == 200
    assert await response.text() == 'Ok'

@pytest.mark.asyncio
async def test_handler_with_different_appname(router):
    appname = "another_app"
    handler = make_handler(appname)
    router.add_route("GET", r"/{one}/{two:.+}", handler)

    request = await aiohttp.test_utils.make_mocked_request("GET", "/3/4", app=web.Application())
    response = await handler(request)
    
    assert response.status == 200
    assert await response.text() == 'Ok'

@pytest.mark.asyncio
async def test_handler_with_empty_values(router):
    appname = "empty_app"
    handler = make_handler(appname)
    router.add_route("GET", r"/{one}/{two:.+}", handler)

    request = await aiohttp.test_utils.make_mocked_request("GET", "/5/", app=web.Application())
    response = await handler(request)
    
    assert response.status == 200
    assert await response.text() == 'Ok'

@pytest.mark.asyncio
async def test_handler_with_invalid_route(router):
    appname = "invalid_app"
    handler = make_handler(appname)
    router.add_route("GET", r"/{one}/{two:.+}", handler)

    request = await aiohttp.test_utils.make_mocked_request("GET", "/invalid_route", app=web.Application())
    response = await handler(request)
    
    assert response.status == 404  # Assuming the route does not match

@pytest.mark.asyncio
async def test_handler_with_special_characters(router):
    appname = "special_app"
    handler = make_handler(appname)
    router.add_route("GET", r"/{one}/{two:.+}", handler)

    request = await aiohttp.test_utils.make_mocked_request("GET", "/!@#/^&*", app=web.Application())
    response = await handler(request)
    
    assert response.status == 200
    assert await response.text() == 'Ok'
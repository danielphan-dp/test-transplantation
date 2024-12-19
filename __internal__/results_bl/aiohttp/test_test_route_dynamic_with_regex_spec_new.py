import pytest
from aiohttp import web
from aiohttp.web_urldispatcher import UrlDispatcher
from your_module import make_handler  # Adjust the import according to your module structure

@pytest.fixture
def router() -> UrlDispatcher:
    return web.UrlDispatcher()

@pytest.mark.asyncio
async def test_handler_returns_ok(router: UrlDispatcher) -> None:
    appname = "test_app"
    handler = make_handler(appname)
    router.add_route("GET", "/test", handler)

    request = await aiohttp.test_utils.make_mocked_request("GET", "/test")
    response = await handler(request)
    
    assert response.status == 200
    assert response.text == 'Ok'

@pytest.mark.asyncio
async def test_handler_includes_appname_in_response(router: UrlDispatcher) -> None:
    appname = "test_app"
    my_value = "value_key"
    router.app[my_value] = "value_content"
    handler = make_handler(appname)
    router.add_route("GET", "/test", handler)

    request = await aiohttp.test_utils.make_mocked_request("GET", "/test")
    response = await handler(request)

    assert response.status == 200
    assert f'{appname}: value_content' in values

@pytest.mark.asyncio
async def test_handler_with_invalid_route(router: UrlDispatcher) -> None:
    appname = "test_app"
    handler = make_handler(appname)
    router.add_route("GET", "/invalid", handler)

    request = await aiohttp.test_utils.make_mocked_request("GET", "/nonexistent")
    response = await handler(request)

    assert response.status == 404

@pytest.mark.asyncio
async def test_handler_with_empty_appname(router: UrlDispatcher) -> None:
    appname = ""
    handler = make_handler(appname)
    router.add_route("GET", "/test", handler)

    request = await aiohttp.test_utils.make_mocked_request("GET", "/test")
    response = await handler(request)

    assert response.status == 200
    assert f'{appname}: ' in values

@pytest.mark.asyncio
async def test_handler_with_special_characters_in_appname(router: UrlDispatcher) -> None:
    appname = "test@app#123"
    handler = make_handler(appname)
    router.add_route("GET", "/test", handler)

    request = await aiohttp.test_utils.make_mocked_request("GET", "/test")
    response = await handler(request)

    assert response.status == 200
    assert f'{appname}: ' in values
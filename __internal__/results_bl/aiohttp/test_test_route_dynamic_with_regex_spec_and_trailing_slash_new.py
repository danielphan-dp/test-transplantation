import pytest
from aiohttp import web
from aiohttp.web_urldispatcher import UrlDispatcher
from your_module import make_handler  # Adjust the import according to your module structure

@pytest.fixture
def router() -> UrlDispatcher:
    return web.UrlDispatcher()

@pytest.mark.asyncio
async def test_handler_returns_ok(router: UrlDispatcher) -> None:
    values = []
    appname = "test_app"
    handler = make_handler(appname)
    router.add_route("GET", "/test", handler)

    request = await aiohttp.test_utils.make_mocked_request("GET", "/test", app=web.Application())
    response = await handler(request)

    assert response.status == 200
    assert await response.text() == 'Ok'
    assert values == [f'{appname}: {request.app.get("my_value", None)}']

@pytest.mark.asyncio
async def test_handler_with_missing_my_value(router: UrlDispatcher) -> None:
    values = []
    appname = "test_app"
    handler = make_handler(appname)
    router.add_route("GET", "/test", handler)

    request = await aiohttp.test_utils.make_mocked_request("GET", "/test", app=web.Application())
    response = await handler(request)

    assert response.status == 200
    assert await response.text() == 'Ok'
    assert values == [f'{appname}: None']

@pytest.mark.asyncio
async def test_handler_with_different_appname(router: UrlDispatcher) -> None:
    values = []
    appname = "another_app"
    handler = make_handler(appname)
    router.add_route("GET", "/test", handler)

    request = await aiohttp.test_utils.make_mocked_request("GET", "/test", app=web.Application())
    response = await handler(request)

    assert response.status == 200
    assert await response.text() == 'Ok'
    assert values == [f'{appname}: {request.app.get("my_value", None)}']
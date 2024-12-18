import pytest
from aiohttp import web
from aiohttp.web import Request
from aiohttp.web_urldispatcher import UrlDispatcher

@pytest.fixture
def router() -> UrlDispatcher:
    return web.UrlDispatcher()

@pytest.mark.asyncio
async def test_make_handler_returns_ok(router: UrlDispatcher) -> None:
    values = []
    appname = "test_app"
    handler = make_handler(appname)

    async def mock_handler(request: Request) -> web.Response:
        return await handler(request)

    router.add_route("GET", "/", mock_handler)

    request = await aiohttp.test_utils.make_mocked_request("GET", "/")
    request.app = {my_value: "test_value"}
    response = await mock_handler(request)

    assert response.status == 200
    assert await response.text() == 'Ok'
    assert values == [f'{appname}: test_value']

@pytest.mark.asyncio
async def test_make_handler_with_different_appname(router: UrlDispatcher) -> None:
    values = []
    appname = "another_app"
    handler = make_handler(appname)

    async def mock_handler(request: Request) -> web.Response:
        return await handler(request)

    router.add_route("GET", "/", mock_handler)

    request = await aiohttp.test_utils.make_mocked_request("GET", "/")
    request.app = {my_value: "another_value"}
    response = await mock_handler(request)

    assert response.status == 200
    assert await response.text() == 'Ok'
    assert values == [f'{appname}: another_value']

@pytest.mark.asyncio
async def test_make_handler_no_value_in_app(router: UrlDispatcher) -> None:
    values = []
    appname = "test_app"
    handler = make_handler(appname)

    async def mock_handler(request: Request) -> web.Response:
        return await handler(request)

    router.add_route("GET", "/", mock_handler)

    request = await aiohttp.test_utils.make_mocked_request("GET", "/")
    request.app = {}
    response = await mock_handler(request)

    assert response.status == 200
    assert await response.text() == 'Ok'
    assert values == [f'{appname}: None']  # Assuming my_value is not found in app

@pytest.mark.asyncio
async def test_make_handler_non_coroutine(router: UrlDispatcher) -> None:
    def handler(request: Request) -> NoReturn:
        assert False

    with pytest.raises(AssertionError):
        router.add_route("GET", "/", make_handler("test_app"), expect_handler=handler)
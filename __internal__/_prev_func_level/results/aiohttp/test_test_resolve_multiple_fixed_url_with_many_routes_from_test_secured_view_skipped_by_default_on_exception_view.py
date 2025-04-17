import asyncio
from unittest import mock
import pytest
from aiohttp import web
from aiohttp.http import HttpVersion
from aiohttp.http import RawRequestMessage
from multidict import CIMultiDict, CIMultiDictProxy
from yarl import URL

def _mock_request(method: str, path: str) -> web.Request:
    message = RawRequestMessage(method, path, HttpVersion(1, 1), CIMultiDictProxy(CIMultiDict()), (), False, None, False, False, URL(path))
    return web.Request(message, mock.Mock(), mock.Mock(), mock.Mock(), mock.Mock(), mock.Mock())

@pytest.fixture
def app(loop: asyncio.AbstractEventLoop) -> web.Application:
    return web.Application()

@pytest.mark.asyncio
async def test_resolve_single_fixed_url(app: web.Application) -> None:
    async def handler(request: web.Request) -> web.Response:
        return web.Response(text="Hello, World!")

    app.router.add_route("GET", "/api/server/dispatch/1/update", handler)
    request = _mock_request(method="GET", path="/api/server/dispatch/1/update")
    match_info = await app.router.resolve(request)
    
    assert match_info is not None
    assert match_info.get_info()["path"] == "/api/server/dispatch/1/update"

@pytest.mark.asyncio
async def test_resolve_invalid_url(app: web.Application) -> None:
    async def handler(request: web.Request) -> web.Response:
        return web.Response(text="Not Found", status=404)

    app.router.add_route("GET", "/api/server/dispatch/2/update", handler)
    request = _mock_request(method="GET", path="/api/server/dispatch/invalid/update")
    
    with pytest.raises(web.HTTPNotFound):
        await app.router.resolve(request)

@pytest.mark.asyncio
async def test_resolve_multiple_routes_with_different_methods(app: web.Application) -> None:
    async def get_handler(request: web.Request) -> web.Response:
        return web.Response(text="GET Response")

    async def post_handler(request: web.Request) -> web.Response:
        return web.Response(text="POST Response")

    app.router.add_route("GET", "/api/server/dispatch/3/update", get_handler)
    app.router.add_route("POST", "/api/server/dispatch/3/update", post_handler)

    get_request = _mock_request(method="GET", path="/api/server/dispatch/3/update")
    post_request = _mock_request(method="POST", path="/api/server/dispatch/3/update")

    get_match_info = await app.router.resolve(get_request)
    post_match_info = await app.router.resolve(post_request)

    assert get_match_info is not None
    assert post_match_info is not None
    assert get_match_info.get_info()["path"] == "/api/server/dispatch/3/update"
    assert post_match_info.get_info()["path"] == "/api/server/dispatch/3/update"

@pytest.mark.asyncio
async def test_resolve_with_query_parameters(app: web.Application) -> None:
    async def handler(request: web.Request) -> web.Response:
        return web.Response(text="Query Received")

    app.router.add_route("GET", "/api/server/dispatch/4/update", handler)
    request = _mock_request(method="GET", path="/api/server/dispatch/4/update?a=1&b=2")
    
    match_info = await app.router.resolve(request)
    
    assert match_info is not None
    assert match_info.get_info()["path"] == "/api/server/dispatch/4/update"
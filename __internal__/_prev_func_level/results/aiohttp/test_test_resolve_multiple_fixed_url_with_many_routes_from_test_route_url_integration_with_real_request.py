import asyncio
import pytest
from unittest import mock
from aiohttp import web
from aiohttp.http import HttpVersion
from aiohttp.http import RawRequestMessage
from multidict import CIMultiDictProxy, CIMultiDict
from yarl import URL

def _mock_request(method: str, path: str) -> web.Request:
    message = RawRequestMessage(method, path, HttpVersion(1, 1), CIMultiDictProxy(CIMultiDict()), (), False, None, False, False, URL(path))
    return web.Request(message, mock.Mock(), mock.Mock(), mock.Mock(), mock.Mock(), mock.Mock())

@pytest.fixture
def app(loop: asyncio.AbstractEventLoop) -> web.Application:
    return web.Application()

@pytest.mark.asyncio
async def test_resolve_single_fixed_url(app: web.Application) -> None:
    """Test resolving a single fixed URL."""
    
    async def handler(request: web.Request) -> web.Response:
        return web.Response(text="Success")

    app.router.add_route("GET", "/api/server/dispatch/1/update", handler)
    app.freeze()
    request = _mock_request(method="GET", path="/api/server/dispatch/1/update")

    match_info = await app.router.resolve(request)
    assert match_info is not None
    assert match_info.get_info()["path"] == "/api/server/dispatch/1/update"

@pytest.mark.asyncio
async def test_resolve_nonexistent_url(app: web.Application) -> None:
    """Test resolving a nonexistent URL."""
    
    async def handler(request: web.Request) -> web.Response:
        return web.Response(text="Success")

    app.router.add_route("GET", "/api/server/dispatch/2/update", handler)
    app.freeze()
    request = _mock_request(method="GET", path="/api/server/dispatch/999/update")

    with pytest.raises(web.HTTPNotFound):
        await app.router.resolve(request)

@pytest.mark.asyncio
async def test_resolve_multiple_routes(app: web.Application) -> None:
    """Test resolving multiple routes."""
    
    async def handler(request: web.Request) -> web.Response:
        return web.Response(text="Success")

    for count in range(5):
        app.router.add_route("GET", f"/api/server/dispatch/{count}/update", handler)
    app.freeze()

    requests = [
        _mock_request(method="GET", path=f"/api/server/dispatch/{count}/update")
        for count in range(5)
    ]

    for request in requests:
        match_info = await app.router.resolve(request)
        assert match_info is not None
        assert match_info.get_info()["path"] == request.path

@pytest.mark.asyncio
async def test_resolve_with_query_params(app: web.Application) -> None:
    """Test resolving a URL with query parameters."""
    
    async def handler(request: web.Request) -> web.Response:
        return web.Response(text="Success")

    app.router.add_route("GET", "/api/server/dispatch/3/update", handler)
    app.freeze()
    request = _mock_request(method="GET", path="/api/server/dispatch/3/update?a=1&b=2")

    match_info = await app.router.resolve(request)
    assert match_info is not None
    assert match_info.get_info()["path"] == "/api/server/dispatch/3/update"
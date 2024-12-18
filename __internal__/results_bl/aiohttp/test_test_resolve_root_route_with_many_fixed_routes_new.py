import asyncio
from unittest import mock
import pytest
from aiohttp import web
from aiohttp.http import HttpVersion
from aiohttp.http import RawRequestMessage
from multidict import CIMultiDictProxy
from yarl import URL

def _mock_request(method: str, path: str) -> web.Request:
    message = RawRequestMessage(method, path, HttpVersion(1, 1), CIMultiDictProxy(CIMultiDict()), (), False, None, False, False, URL(path))
    return web.Request(message, mock.Mock(), mock.Mock(), mock.Mock(), mock.Mock(), mock.Mock())

@pytest.mark.asyncio
async def test_resolve_nonexistent_route(loop: asyncio.AbstractEventLoop) -> None:
    """Test resolving a route that does not exist."""
    app = web.Application()
    
    async def handler(request: web.Request) -> None:
        return web.Response(text="Hello, world")

    app.router.add_route("GET", "/existing", handler)
    request = _mock_request(method="GET", path="/nonexistent")
    
    with pytest.raises(web.HTTPNotFound):
        await app.router.resolve(request)

@pytest.mark.asyncio
async def test_resolve_route_with_query_params(loop: asyncio.AbstractEventLoop) -> None:
    """Test resolving a route with query parameters."""
    app = web.Application()
    
    async def handler(request: web.Request) -> web.Response:
        return web.Response(text="Query received")

    app.router.add_route("GET", "/search", handler)
    request = _mock_request(method="GET", path="/search?query=test")
    
    match_info = await app.router.resolve(request)
    assert match_info is not None
    assert match_info.route.path == "/search"

@pytest.mark.asyncio
async def test_resolve_root_route_with_different_method(loop: asyncio.AbstractEventLoop) -> None:
    """Test resolving root route with a POST method."""
    app = web.Application()
    
    async def handler(request: web.Request) -> web.Response:
        return web.Response(text="Root POST")

    app.router.add_route("POST", "/", handler)
    request = _mock_request(method="POST", path="/")
    
    match_info = await app.router.resolve(request)
    assert match_info is not None
    assert match_info.route.path == "/"

@pytest.mark.asyncio
async def test_resolve_root_route_with_invalid_method(loop: asyncio.AbstractEventLoop) -> None:
    """Test resolving root route with an invalid method."""
    app = web.Application()
    
    async def handler(request: web.Request) -> None:
        return web.Response(text="Should not reach here")

    app.router.add_route("GET", "/", handler)
    request = _mock_request(method="DELETE", path="/")
    
    with pytest.raises(web.HTTPMethodNotAllowed):
        await app.router.resolve(request)
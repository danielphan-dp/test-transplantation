import asyncio
from unittest import mock
import pytest
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

def test_resolve_nonexistent_route(app: web.Application, loop: asyncio.AbstractEventLoop) -> None:
    async def handler(request: web.Request) -> web.Response:
        return web.Response(text="Hello, World!")

    app.router.add_route("GET", "/hello", handler)
    request = _mock_request(method="GET", path="/nonexistent")
    
    async def run_url_dispatcher() -> Optional[web.UrlMappingMatchInfo]:
        return await app.router.resolve(request)

    ret = loop.run_until_complete(run_url_dispatcher())
    assert ret is None

def test_resolve_route_with_query_params(app: web.Application, loop: asyncio.AbstractEventLoop) -> None:
    async def handler(request: web.Request) -> web.Response:
        return web.Response(text="Query Params Received")

    app.router.add_route("GET", "/query", handler)
    request = _mock_request(method="GET", path="/query?a=1&b=2")
    
    async def run_url_dispatcher() -> Optional[web.UrlMappingMatchInfo]:
        return await app.router.resolve(request)

    ret = loop.run_until_complete(run_url_dispatcher())
    assert ret is not None
    assert ret.get_info()["path"] == "/query", ret.get_info()

def test_resolve_root_route_with_invalid_method(app: web.Application, loop: asyncio.AbstractEventLoop) -> None:
    async def handler(request: web.Request) -> web.Response:
        return web.Response(text="This should not be reached")

    app.router.add_route("GET", "/", handler)
    request = _mock_request(method="POST", path="/")
    
    async def run_url_dispatcher() -> Optional[web.UrlMappingMatchInfo]:
        return await app.router.resolve(request)

    ret = loop.run_until_complete(run_url_dispatcher())
    assert ret is None

def test_resolve_multiple_routes(app: web.Application, loop: asyncio.AbstractEventLoop) -> None:
    async def handler(request: web.Request) -> web.Response:
        return web.Response(text="Handled")

    for count in range(5):
        app.router.add_route("GET", f"/route/{count}", handler)

    request = _mock_request(method="GET", path="/route/3")
    
    async def run_url_dispatcher() -> Optional[web.UrlMappingMatchInfo]:
        return await app.router.resolve(request)

    ret = loop.run_until_complete(run_url_dispatcher())
    assert ret is not None
    assert ret.get_info()["path"] == "/route/3", ret.get_info()
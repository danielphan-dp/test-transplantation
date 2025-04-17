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

def test_resolve_single_fixed_url(app: web.Application, loop: asyncio.AbstractEventLoop) -> None:
    async def handler(request: web.Request) -> web.Response:
        return web.Response(text="Success")

    app.router.add_route("GET", "/api/server/dispatch/1/update", handler)
    app.freeze()
    request = _mock_request(method="GET", path="/api/server/dispatch/1/update")

    async def run_url_dispatcher() -> web.UrlMappingMatchInfo:
        return await app.router.resolve(request)

    ret = loop.run_until_complete(run_url_dispatcher())
    assert ret is not None
    assert ret.get_info()["path"] == "/api/server/dispatch/1/update", ret.get_info()

def test_resolve_invalid_url(app: web.Application, loop: asyncio.AbstractEventLoop) -> None:
    async def handler(request: web.Request) -> web.Response:
        return web.Response(text="Success")

    app.router.add_route("GET", "/api/server/dispatch/1/update", handler)
    app.freeze()
    request = _mock_request(method="GET", path="/api/server/dispatch/invalid/update")

    async def run_url_dispatcher() -> web.UrlMappingMatchInfo:
        return await app.router.resolve(request)

    with pytest.raises(web.HTTPNotFound):
        loop.run_until_complete(run_url_dispatcher())

def test_resolve_multiple_fixed_url_with_edge_cases(app: web.Application, loop: asyncio.AbstractEventLoop) -> None:
    async def handler(request: web.Request) -> web.Response:
        return web.Response(text="Success")

    for count in range(5):
        app.router.add_route("GET", f"/api/server/dispatch/{count}/update", handler)
    app.freeze()

    requests = [
        _mock_request(method="GET", path=f"/api/server/dispatch/{count}/update")
        for count in range(5)
    ]

    async def run_url_dispatcher() -> Optional[web.UrlMappingMatchInfo]:
        ret = None
        for request in requests:
            ret = await app.router.resolve(request)
        return ret

    ret = loop.run_until_complete(run_url_dispatcher())
    assert ret is not None
    assert ret.get_info()["path"] == "/api/server/dispatch/4/update", ret.get_info()
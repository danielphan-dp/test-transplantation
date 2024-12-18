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
async def test_resolve_invalid_method(loop: asyncio.AbstractEventLoop) -> None:
    app = web.Application()
    app.router.add_route("GET", "/api/server/dispatch/0/update", lambda request: web.Response(text="OK"))
    app.freeze()
    router = app.router

    request = _mock_request(method="POST", path="/api/server/dispatch/0/update")
    
    with pytest.raises(web.HTTPMethodNotAllowed):
        await router.resolve(request)

@pytest.mark.asyncio
async def test_resolve_nonexistent_route(loop: asyncio.AbstractEventLoop) -> None:
    app = web.Application()
    app.router.add_route("GET", "/api/server/dispatch/0/update", lambda request: web.Response(text="OK"))
    app.freeze()
    router = app.router

    request = _mock_request(method="GET", path="/api/server/dispatch/999/update")
    
    with pytest.raises(web.HTTPNotFound):
        await router.resolve(request)

@pytest.mark.asyncio
async def test_resolve_multiple_fixed_url_with_edge_cases(loop: asyncio.AbstractEventLoop) -> None:
    async def handler(request: web.Request) -> web.Response:
        return web.Response(text="Handled")

    app = web.Application()
    for count in range(5):
        app.router.add_route("GET", f"/api/server/dispatch/{count}/update", handler)
    app.freeze()
    router = app.router

    requests = [
        _mock_request(method="GET", path=f"/api/server/dispatch/{count}/update")
        for count in range(5)
    ]

    for request in requests:
        ret = await router.resolve(request)
        assert ret.status == 200
        assert await ret.text() == "Handled"

@pytest.mark.asyncio
async def test_resolve_empty_path(loop: asyncio.AbstractEventLoop) -> None:
    app = web.Application()
    app.router.add_route("GET", "/", lambda request: web.Response(text="Root"))
    app.freeze()
    router = app.router

    request = _mock_request(method="GET", path="/")
    ret = await router.resolve(request)
    assert ret.status == 200
    assert await ret.text() == "Root"
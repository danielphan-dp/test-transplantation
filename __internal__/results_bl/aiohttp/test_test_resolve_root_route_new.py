import asyncio
from unittest import mock
import pytest
from multidict import CIMultiDict, CIMultiDictProxy
from aiohttp import web
from aiohttp.http import HttpVersion
from aiohttp.http import RawRequestMessage
from yarl import URL

def _mock_request(method: str, path: str) -> web.Request:
    message = RawRequestMessage(method, path, HttpVersion(1, 1), CIMultiDictProxy(CIMultiDict()), (), False, None, False, False, URL(path))
    return web.Request(message, mock.Mock(), mock.Mock(), mock.Mock(), mock.Mock(), mock.Mock())

@pytest.mark.asyncio
async def test_mock_request_get():
    request = _mock_request(method="GET", path="/test")
    assert request.method == "GET"
    assert request.path == "/test"

@pytest.mark.asyncio
async def test_mock_request_post():
    request = _mock_request(method="POST", path="/submit")
    assert request.method == "POST"
    assert request.path == "/submit"

@pytest.mark.asyncio
async def test_mock_request_invalid_method():
    request = _mock_request(method="INVALID", path="/error")
    assert request.method == "INVALID"
    assert request.path == "/error"

@pytest.mark.asyncio
async def test_mock_request_empty_path():
    request = _mock_request(method="GET", path="")
    assert request.method == "GET"
    assert request.path == ""

@pytest.mark.asyncio
async def test_mock_request_special_characters():
    request = _mock_request(method="GET", path="/test?query=1&value=2")
    assert request.method == "GET"
    assert request.path == "/test?query=1&value=2"

@pytest.mark.asyncio
async def test_resolve_nonexistent_route(loop: asyncio.AbstractEventLoop):
    async def handler(request: web.Request) -> None:
        return web.Response(text="Not Found", status=404)

    app = web.Application()
    app.router.add_route("GET", "/notfound", handler)
    app.freeze()
    router = app.router
    request = _mock_request(method="GET", path="/nonexistent")

    async def run_url_dispatcher():
        return await router.resolve(request)

    with pytest.raises(web.HTTPNotFound):
        loop.run_until_complete(run_url_dispatcher())
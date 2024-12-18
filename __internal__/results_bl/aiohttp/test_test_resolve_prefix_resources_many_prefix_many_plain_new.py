import asyncio
import pytest
from unittest import mock
from aiohttp import web
from aiohttp.http import HttpVersion
from aiohttp.http import RawRequestMessage
from multidict import CIMultiDictProxy
from yarl import URL

def _mock_request(method: str, path: str) -> web.Request:
    message = RawRequestMessage(method, path, HttpVersion(1, 1), CIMultiDictProxy(CIMultiDict()), (), False, None, False, False, URL(path))
    return web.Request(message, mock.Mock(), mock.Mock(), mock.Mock(), mock.Mock(), mock.Mock())

@pytest.mark.asyncio
async def test_mock_request_get():
    request = _mock_request("GET", "/test/path")
    assert request.method == "GET"
    assert request.path == "/test/path"

@pytest.mark.asyncio
async def test_mock_request_post():
    request = _mock_request("POST", "/test/path")
    assert request.method == "POST"
    assert request.path == "/test/path"

@pytest.mark.asyncio
async def test_mock_request_invalid_method():
    request = _mock_request("INVALID", "/test/path")
    assert request.method == "INVALID"
    assert request.path == "/test/path"

@pytest.mark.asyncio
async def test_mock_request_empty_path():
    request = _mock_request("GET", "")
    assert request.method == "GET"
    assert request.path == ""

@pytest.mark.asyncio
async def test_mock_request_long_path():
    long_path = "/test/" + "a" * 1000
    request = _mock_request("GET", long_path)
    assert request.method == "GET"
    assert request.path == long_path

@pytest.mark.asyncio
async def test_resolve_prefix_resources_edge_case(loop: asyncio.AbstractEventLoop):
    async def handler(request: web.Request) -> None:
        return web.Response(text="Handled")

    app = web.Application()
    app.router.add_get("/api/edge/case", handler)
    app.freeze()
    router = app.router

    request = _mock_request(method="GET", path="/api/edge/case")
    ret = await router.resolve(request)
    assert ret is not None
    assert ret.get_info()["path"] == "/api/edge/case", ret.get_info()
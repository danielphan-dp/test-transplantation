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
async def test_mock_request_with_invalid_method():
    request = _mock_request(method="INVALID", path="/api/server/dispatch/1/update")
    assert request.method == "INVALID"
    assert request.path == "/api/server/dispatch/1/update"

@pytest.mark.asyncio
async def test_mock_request_with_empty_path():
    request = _mock_request(method="GET", path="")
    assert request.method == "GET"
    assert request.path == ""

@pytest.mark.asyncio
async def test_mock_request_with_special_characters():
    request = _mock_request(method="GET", path="/api/server/dispatch/1/update?query=param&value=1")
    assert request.method == "GET"
    assert request.path == "/api/server/dispatch/1/update?query=param&value=1"

@pytest.mark.asyncio
async def test_mock_request_with_long_path():
    long_path = "/api/" + "a" * 1000 + "/dispatch/1/update"
    request = _mock_request(method="GET", path=long_path)
    assert request.method == "GET"
    assert request.path == long_path

@pytest.mark.asyncio
async def test_mock_request_with_nonexistent_route():
    app = web.Application()
    request = _mock_request(method="GET", path="/api/nonexistent")
    with pytest.raises(web.HTTPNotFound):
        await app.router.resolve(request)
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

def test_mock_request_get(app: web.Application) -> None:
    request = _mock_request("GET", "/test/path")
    assert request.method == "GET"
    assert request.path == "/test/path"
    assert request.version == HttpVersion(1, 1)

def test_mock_request_post(app: web.Application) -> None:
    request = _mock_request("POST", "/test/path")
    assert request.method == "POST"
    assert request.path == "/test/path"
    assert request.version == HttpVersion(1, 1)

def test_mock_request_with_headers(app: web.Application) -> None:
    headers = CIMultiDict({"Content-Type": "application/json"})
    request = _mock_request("GET", "/test/path")
    request.headers = headers
    assert request.headers["Content-Type"] == "application/json"

def test_mock_request_invalid_method(app: web.Application) -> None:
    with pytest.raises(ValueError):
        _mock_request("INVALID", "/test/path")

def test_mock_request_empty_path(app: web.Application) -> None:
    request = _mock_request("GET", "")
    assert request.path == ""

def test_mock_request_query_string(app: web.Application) -> None:
    request = _mock_request("GET", "/test/path?a=1&b=2")
    assert request.path_qs == "/test/path?a=1&b=2"
    assert request.query_string == "a=1&b=2"
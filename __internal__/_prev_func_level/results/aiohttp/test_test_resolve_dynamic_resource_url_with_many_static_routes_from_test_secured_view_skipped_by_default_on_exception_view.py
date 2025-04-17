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

def test_mock_request_creation(app: web.Application) -> None:
    req = _mock_request("GET", "/test/path")
    
    assert req.method == "GET"
    assert req.path == "/test/path"
    assert req.version == HttpVersion(1, 1)
    assert req.keep_alive is True
    assert req.headers == CIMultiDictProxy(CIMultiDict())
    assert req.raw_headers == ()

def test_mock_request_with_headers(app: web.Application) -> None:
    headers = CIMultiDict({"Content-Type": "application/json"})
    req = _mock_request("POST", "/test/path")
    req.headers = headers

    assert req.headers.get("Content-Type") == "application/json"

def test_mock_request_with_invalid_method(app: web.Application) -> None:
    with pytest.raises(ValueError):
        _mock_request("INVALID_METHOD", "/test/path")

def test_mock_request_path_with_query_string(app: web.Application) -> None:
    req = _mock_request("GET", "/test/path?query=1")
    
    assert req.path_qs == "/test/path?query=1"
    assert req.query_string == "query=1"

def test_mock_request_empty_path(app: web.Application) -> None:
    req = _mock_request("GET", "")
    
    assert req.path == ""
    assert req.path_qs == ""
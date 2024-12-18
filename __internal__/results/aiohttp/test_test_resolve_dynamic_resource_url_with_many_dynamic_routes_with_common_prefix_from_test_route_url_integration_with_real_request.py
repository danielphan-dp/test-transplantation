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

def test_mock_request_with_valid_method_and_path(app: web.Application) -> None:
    request = _mock_request("GET", "/test/path")
    assert request.method == "GET"
    assert request.path == "/test/path"
    assert request.version == HttpVersion(1, 1)

def test_mock_request_with_invalid_method(app: web.Application) -> None:
    request = _mock_request("INVALID", "/test/path")
    assert request.method == "INVALID"
    assert request.path == "/test/path"

def test_mock_request_with_query_string(app: web.Application) -> None:
    request = _mock_request("GET", "/test/path?a=1&b=2")
    assert request.path_qs == "/test/path?a=1&b=2"
    assert request.query_string == "a=1&b=2"

def test_mock_request_with_headers(app: web.Application) -> None:
    headers = CIMultiDict({"Content-Type": "application/json"})
    request = _mock_request("GET", "/test/path")
    request.headers = headers
    assert request.headers["Content-Type"] == "application/json"

def test_mock_request_with_empty_path(app: web.Application) -> None:
    request = _mock_request("GET", "")
    assert request.path == ""

def test_mock_request_with_special_characters(app: web.Application) -> None:
    request = _mock_request("GET", "/test/path/with space")
    assert request.path == "/test/path/with space"

def test_mock_request_with_long_path(app: web.Application) -> None:
    long_path = "/test/" + "a" * 1000
    request = _mock_request("GET", long_path)
    assert request.path == long_path

def test_mock_request_with_multiple_slashes(app: web.Application) -> None:
    request = _mock_request("GET", "/test//path")
    assert request.path == "/test//path"
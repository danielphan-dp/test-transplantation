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

def test_mock_request_with_invalid_method(app: web.Application) -> None:
    request = _mock_request(method="INVALID", path="/api/test")
    assert request.method == "INVALID"
    assert request.path == "/api/test"

def test_mock_request_with_query_parameters(app: web.Application) -> None:
    request = _mock_request(method="GET", path="/api/test?param1=value1&param2=value2")
    assert request.query_string == "param1=value1&param2=value2"
    assert request.query.get("param1") == "value1"
    assert request.query.get("param2") == "value2"

def test_mock_request_with_headers(app: web.Application) -> None:
    headers = CIMultiDict({"Content-Type": "application/json"})
    request = _mock_request(method="POST", path="/api/test")
    request.headers.update(headers)
    assert request.headers["Content-Type"] == "application/json"

def test_mock_request_with_path_and_method(app: web.Application) -> None:
    request = _mock_request(method="GET", path="/api/test")
    assert request.path == "/api/test"
    assert request.method == "GET"

def test_mock_request_with_empty_path(app: web.Application) -> None:
    request = _mock_request(method="GET", path="")
    assert request.path == ""
    assert request.method == "GET"

def test_mock_request_with_unsupported_http_version(app: web.Application) -> None:
    request = _mock_request(method="GET", path="/api/test")
    assert request.version == HttpVersion(1, 1)

def test_mock_request_with_multiple_requests(app: web.Application) -> None:
    for count in range(5):
        request = _mock_request(method="GET", path=f"/api/test/{count}")
        assert request.path == f"/api/test/{count}"
        assert request.method == "GET"
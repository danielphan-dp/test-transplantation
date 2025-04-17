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
    request = _mock_request(method="INVALID", path="/")
    assert request.method == "INVALID"
    assert request.path == "/"

def test_mock_request_with_query_parameters(app: web.Application) -> None:
    request = _mock_request(method="GET", path="/test?param=value")
    assert request.path_qs == "/test?param=value"
    assert request.query_string == "param=value"

def test_mock_request_with_headers(app: web.Application) -> None:
    headers = CIMultiDict({"Content-Type": "application/json"})
    request = _mock_request(method="GET", path="/", headers=headers)
    assert request.headers["Content-Type"] == "application/json"

def test_mock_request_with_path_and_method(app: web.Application) -> None:
    request = _mock_request(method="POST", path="/submit")
    assert request.method == "POST"
    assert request.path == "/submit"

def test_mock_request_with_empty_path(app: web.Application) -> None:
    request = _mock_request(method="GET", path="")
    assert request.path == ""

def test_mock_request_with_unsupported_http_version(app: web.Application) -> None:
    request = _mock_request(method="GET", path="/", version=HttpVersion(0, 9))
    assert request.version == HttpVersion(0, 9)

def test_mock_request_with_multiple_slashes(app: web.Application) -> None:
    request = _mock_request(method="GET", path="/foo//bar")
    assert request.path == "/foo//bar"
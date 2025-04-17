import asyncio
from unittest import mock
import pytest
from aiohttp import web
from aiohttp.http import HttpVersion
from aiohttp.http import RawRequestMessage
from multidict import CIMultiDict, CIMultiDictProxy
from yarl import URL

def _mock_request(method: str, path: str) -> web.Request:
    message = RawRequestMessage(method, path, HttpVersion(1, 1), CIMultiDictProxy(CIMultiDict()), (), False, None, False, False, URL(path))
    return web.Request(message, mock.Mock(), mock.Mock(), mock.Mock(), mock.Mock(), mock.Mock())

@pytest.fixture
def app(loop: asyncio.AbstractEventLoop) -> web.Application:
    return web.Application()

def test_mock_request_get(app: web.Application, loop: asyncio.AbstractEventLoop) -> None:
    request = _mock_request(method="GET", path="/test")
    assert request.method == "GET"
    assert request.path == "/test"
    assert request.version == HttpVersion(1, 1)

def test_mock_request_post(app: web.Application, loop: asyncio.AbstractEventLoop) -> None:
    request = _mock_request(method="POST", path="/submit")
    assert request.method == "POST"
    assert request.path == "/submit"

def test_mock_request_with_headers(app: web.Application, loop: asyncio.AbstractEventLoop) -> None:
    headers = CIMultiDict({"Content-Type": "application/json"})
    request = _mock_request(method="GET", path="/data")
    request.headers = headers
    assert request.headers["Content-Type"] == "application/json"

def test_mock_request_invalid_method(app: web.Application, loop: asyncio.AbstractEventLoop) -> None:
    with pytest.raises(ValueError):
        _mock_request(method="INVALID", path="/")

def test_mock_request_empty_path(app: web.Application, loop: asyncio.AbstractEventLoop) -> None:
    request = _mock_request(method="GET", path="")
    assert request.path == ""

def test_mock_request_query_string(app: web.Application, loop: asyncio.AbstractEventLoop) -> None:
    request = _mock_request(method="GET", path="/search?q=test")
    assert request.path_qs == "/search?q=test"
    assert request.query_string == "q=test"
import asyncio
from unittest import mock
from aiohttp import web
from aiohttp.http import HttpVersion
from aiohttp.http import RawRequestMessage
from multidict import CIMultiDictProxy, CIMultiDict
from yarl import URL

def test_mock_request_creates_valid_request() -> None:
    method = "GET"
    path = "/test/path"
    request = _mock_request(method, path)

    assert request.method == method
    assert request.path == path
    assert request.version == HttpVersion(1, 1)
    assert request.keep_alive is True
    assert request.headers == CIMultiDictProxy(CIMultiDict())
    assert request.raw_headers == ()

def test_mock_request_with_custom_headers() -> None:
    method = "POST"
    path = "/test/path"
    headers = CIMultiDict({"Content-Type": "application/json"})
    request = _mock_request(method, path)

    request.headers = headers

    assert request.method == method
    assert request.path == path
    assert request.headers == CIMultiDictProxy(headers)

def test_mock_request_with_invalid_method() -> None:
    method = "INVALID"
    path = "/test/path"
    request = _mock_request(method, path)

    assert request.method == method
    assert request.path == path

def test_mock_request_with_empty_path() -> None:
    method = "GET"
    path = ""
    request = _mock_request(method, path)

    assert request.method == method
    assert request.path == path

def test_mock_request_with_special_characters_in_path() -> None:
    method = "GET"
    path = "/test/path?query=1&value=2"
    request = _mock_request(method, path)

    assert request.method == method
    assert request.path == path
    assert request.query_string == "query=1&value=2"
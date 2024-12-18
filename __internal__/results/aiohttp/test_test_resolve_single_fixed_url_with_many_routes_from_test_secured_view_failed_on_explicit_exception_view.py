import asyncio
from aiohttp import web
from aiohttp.http import HttpVersion, RawRequestMessage
from multidict import CIMultiDict, CIMultiDictProxy
from unittest import mock
import pytest

def test_mock_request_creates_valid_request() -> None:
    method = "POST"
    path = "/api/test"
    request = _mock_request(method=method, path=path)

    assert request.method == method
    assert request.path == path
    assert request.version == HttpVersion(1, 1)
    assert isinstance(request.headers, CIMultiDictProxy)
    assert request.keep_alive

def test_mock_request_with_headers() -> None:
    method = "GET"
    path = "/api/test"
    headers = CIMultiDict({"Content-Type": "application/json"})
    request = _mock_request(method=method, path=path)

    request.headers.update(headers)
    
    assert request.headers.get("Content-Type") == "application/json"

def test_mock_request_invalid_method() -> None:
    method = "INVALID"
    path = "/api/test"
    request = _mock_request(method=method, path=path)

    assert request.method == method
    assert request.path == path

def test_mock_request_empty_path() -> None:
    method = "GET"
    path = ""
    request = _mock_request(method=method, path=path)

    assert request.method == method
    assert request.path == path

def test_mock_request_multiple_requests() -> None:
    method = "GET"
    paths = [f"/api/test/{i}" for i in range(5)]
    requests = [_mock_request(method=method, path=path) for path in paths]

    for i, request in enumerate(requests):
        assert request.method == method
        assert request.path == paths[i]
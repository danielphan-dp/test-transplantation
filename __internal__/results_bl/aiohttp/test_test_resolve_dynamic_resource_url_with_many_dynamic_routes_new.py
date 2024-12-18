import asyncio
from unittest import mock
import pytest
from multidict import CIMultiDictProxy
from aiohttp import web
from aiohttp.http import HttpVersion, RawRequestMessage
from yarl import URL

def _mock_request(method: str, path: str) -> web.Request:
    message = RawRequestMessage(method, path, HttpVersion(1, 1), CIMultiDictProxy(CIMultiDict()), (), False, None, False, False, URL(path))
    return web.Request(message, mock.Mock(), mock.Mock(), mock.Mock(), mock.Mock(), mock.Mock())

@pytest.mark.asyncio
async def test_mock_request_invalid_method():
    request = _mock_request(method="INVALID", path="/api/test")
    assert request.method == "INVALID"
    assert request.path == "/api/test"

@pytest.mark.asyncio
async def test_mock_request_empty_path():
    request = _mock_request(method="GET", path="")
    assert request.method == "GET"
    assert request.path == ""

@pytest.mark.asyncio
async def test_mock_request_special_characters():
    special_path = "/api/test/!@#$%^&*()"
    request = _mock_request(method="GET", path=special_path)
    assert request.method == "GET"
    assert request.path == special_path

@pytest.mark.asyncio
async def test_mock_request_large_path():
    large_path = "/api/" + "a" * 1000
    request = _mock_request(method="GET", path=large_path)
    assert request.method == "GET"
    assert request.path == large_path

@pytest.mark.asyncio
async def test_mock_request_with_query_params():
    request = _mock_request(method="GET", path="/api/test?param=value")
    assert request.method == "GET"
    assert request.path == "/api/test?param=value"
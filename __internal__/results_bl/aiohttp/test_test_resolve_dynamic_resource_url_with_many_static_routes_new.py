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
async def test_mock_request_long_path():
    long_path = "/api/" + "a" * 2048
    request = _mock_request(method="GET", path=long_path)
    assert request.method == "GET"
    assert request.path == long_path

@pytest.mark.asyncio
async def test_mock_request_with_query_params():
    request = _mock_request(method="GET", path="/api/test?param=value")
    assert request.method == "GET"
    assert request.path == "/api/test?param=value"
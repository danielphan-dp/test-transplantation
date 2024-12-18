import asyncio
from unittest import mock
import pytest
from multidict import CIMultiDictProxy
from aiohttp import web
from aiohttp.http import HttpVersion
from aiohttp.http import RawRequestMessage
from yarl import URL

def _mock_request(method: str, path: str) -> web.Request:
    message = RawRequestMessage(method, path, HttpVersion(1, 1), CIMultiDictProxy(CIMultiDict()), (), False, None, False, False, URL(path))
    return web.Request(message, mock.Mock(), mock.Mock(), mock.Mock(), mock.Mock(), mock.Mock())

@pytest.mark.asyncio
async def test_mock_request_with_valid_path():
    request = _mock_request("GET", "/valid/path")
    assert request.method == "GET"
    assert request.path == "/valid/path"

@pytest.mark.asyncio
async def test_mock_request_with_empty_path():
    request = _mock_request("GET", "")
    assert request.method == "GET"
    assert request.path == ""

@pytest.mark.asyncio
async def test_mock_request_with_invalid_method():
    request = _mock_request("INVALID", "/path")
    assert request.method == "INVALID"
    assert request.path == "/path"

@pytest.mark.asyncio
async def test_mock_request_with_special_characters():
    request = _mock_request("GET", "/path/with/special/characters/!@#$%^&*()")
    assert request.method == "GET"
    assert request.path == "/path/with/special/characters/!@#$%^&*()"

@pytest.mark.asyncio
async def test_mock_request_with_long_path():
    long_path = "/a" + "/b" * 100  # Create a long path
    request = _mock_request("GET", long_path)
    assert request.method == "GET"
    assert request.path == long_path

@pytest.mark.asyncio
async def test_mock_request_with_query_parameters():
    request = _mock_request("GET", "/path?query=parameter")
    assert request.method == "GET"
    assert request.path == "/path?query=parameter"
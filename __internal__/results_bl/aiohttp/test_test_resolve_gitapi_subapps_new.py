import asyncio
import random
import string
from unittest import mock
import pytest
from aiohttp import web
from aiohttp.http import HttpVersion, RawRequestMessage
from multidict import CIMultiDictProxy
from yarl import URL

def _mock_request(method: str, path: str) -> web.Request:
    message = RawRequestMessage(method, path, HttpVersion(1, 1), CIMultiDictProxy(CIMultiDict()), (), False, None, False, False, URL(path))
    return web.Request(message, mock.Mock(), mock.Mock(), mock.Mock(), mock.Mock(), mock.Mock())

@pytest.mark.asyncio
async def test_mock_request_valid_method_and_path():
    request = _mock_request("GET", "/valid/path")
    assert request.method == "GET"
    assert request.path == "/valid/path"

@pytest.mark.asyncio
async def test_mock_request_invalid_method():
    request = _mock_request("INVALID", "/path")
    assert request.method == "INVALID"
    assert request.path == "/path"

@pytest.mark.asyncio
async def test_mock_request_empty_path():
    request = _mock_request("GET", "")
    assert request.method == "GET"
    assert request.path == ""

@pytest.mark.asyncio
async def test_mock_request_special_characters_in_path():
    special_path = "/path/with/special/characters/!@#$%^&*()"
    request = _mock_request("GET", special_path)
    assert request.method == "GET"
    assert request.path == special_path

@pytest.mark.asyncio
async def test_mock_request_long_path():
    long_path = "/" + "/".join(["long" for _ in range(100)])
    request = _mock_request("GET", long_path)
    assert request.method == "GET"
    assert request.path == long_path

@pytest.mark.asyncio
async def test_mock_request_multiple_requests():
    requests = [_mock_request("GET", f"/path/{i}") for i in range(5)]
    for i, request in enumerate(requests):
        assert request.method == "GET"
        assert request.path == f"/path/{i}"
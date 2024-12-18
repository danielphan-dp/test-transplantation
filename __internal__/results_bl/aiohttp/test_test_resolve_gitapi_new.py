import asyncio
import string
import random
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
async def test_mock_request_valid_method_and_path():
    request = _mock_request("GET", "/valid/path")
    assert request.method == "GET"
    assert request.path == "/valid/path"

@pytest.mark.asyncio
async def test_mock_request_invalid_method():
    request = _mock_request("INVALID", "/path")
    assert request.method == "INVALID"

@pytest.mark.asyncio
async def test_mock_request_empty_path():
    request = _mock_request("GET", "")
    assert request.path == ""

@pytest.mark.asyncio
async def test_mock_request_special_characters_in_path():
    special_path = "/path/with/special/characters/!@#$%^&*()"
    request = _mock_request("GET", special_path)
    assert request.path == special_path

@pytest.mark.asyncio
async def test_mock_request_long_path():
    long_path = "/a" * 2048
    request = _mock_request("GET", long_path)
    assert request.path == long_path

@pytest.mark.asyncio
async def test_mock_request_multiple_requests():
    requests = []
    for i in range(5):
        requests.append(_mock_request("GET", f"/path/{i}"))
    for i, request in enumerate(requests):
        assert request.path == f"/path/{i}"
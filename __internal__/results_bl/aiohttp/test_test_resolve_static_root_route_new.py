import asyncio
import pathlib
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
async def test_mock_request_get():
    request = _mock_request(method="GET", path="/test")
    assert request.method == "GET"
    assert request.path == "/test"

@pytest.mark.asyncio
async def test_mock_request_post():
    request = _mock_request(method="POST", path="/submit")
    assert request.method == "POST"
    assert request.path == "/submit"

@pytest.mark.asyncio
async def test_mock_request_invalid_method():
    with pytest.raises(ValueError):
        _mock_request(method="INVALID", path="/")

@pytest.mark.asyncio
async def test_mock_request_empty_path():
    request = _mock_request(method="GET", path="")
    assert request.path == ""

@pytest.mark.asyncio
async def test_mock_request_special_characters():
    request = _mock_request(method="GET", path="/test?query=1&value=2")
    assert request.path == "/test?query=1&value=2"
import asyncio
import pathlib
from unittest import mock
import pytest
from multidict import CIMultiDict, CIMultiDictProxy
from aiohttp import web
from aiohttp.http import HttpVersion, RawRequestMessage
from aiohttp.test_utils import make_mocked_request

@pytest.mark.asyncio
async def test_mock_request_get():
    """Test _mock_request with GET method."""
    request = _mock_request(method="GET", path="/test")
    assert request.method == "GET"
    assert request.path == "/test"
    assert request.version == HttpVersion(1, 1)

@pytest.mark.asyncio
async def test_mock_request_post():
    """Test _mock_request with POST method."""
    request = _mock_request(method="POST", path="/submit")
    assert request.method == "POST"
    assert request.path == "/submit"

@pytest.mark.asyncio
async def test_mock_request_with_headers():
    """Test _mock_request with custom headers."""
    headers = CIMultiDict({"Content-Type": "application/json"})
    request = _mock_request(method="GET", path="/data")
    request.headers.update(headers)
    assert request.headers["Content-Type"] == "application/json"

@pytest.mark.asyncio
async def test_mock_request_invalid_method():
    """Test _mock_request with an invalid HTTP method."""
    with pytest.raises(ValueError):
        _mock_request(method="INVALID", path="/")

@pytest.mark.asyncio
async def test_mock_request_empty_path():
    """Test _mock_request with an empty path."""
    request = _mock_request(method="GET", path="")
    assert request.path == ""

@pytest.mark.asyncio
async def test_mock_request_path_with_query():
    """Test _mock_request with a path containing query parameters."""
    request = _mock_request(method="GET", path="/search?q=test")
    assert request.path_qs == "/search?q=test"
    assert request.query_string == "q=test"
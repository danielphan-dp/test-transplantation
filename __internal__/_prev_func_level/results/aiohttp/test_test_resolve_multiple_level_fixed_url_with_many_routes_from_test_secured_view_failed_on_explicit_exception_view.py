import asyncio
from unittest import mock
import pytest
from aiohttp import web
from aiohttp.http import HttpVersion
from aiohttp.http import RawRequestMessage
from multidict import CIMultiDictProxy, CIMultiDict
from yarl import URL

def test_mock_request_creates_valid_request() -> None:
    """Test that _mock_request creates a valid web.Request object."""
    method = "GET"
    path = "/test/path"
    request = _mock_request(method, path)

    assert request.method == method
    assert request.path == path
    assert request.version == HttpVersion(1, 1)
    assert isinstance(request.headers, CIMultiDictProxy)
    assert request.keep_alive is True

def test_mock_request_with_custom_headers() -> None:
    """Test that _mock_request handles custom headers correctly."""
    method = "POST"
    path = "/test/path"
    headers = CIMultiDict({"Content-Type": "application/json"})
    request = _mock_request(method, path)

    request.headers = headers

    assert request.headers.get("Content-Type") == "application/json"

def test_mock_request_invalid_method() -> None:
    """Test that _mock_request raises an error for invalid HTTP methods."""
    method = "INVALID"
    path = "/test/path"
    
    with pytest.raises(ValueError):
        _mock_request(method, path)

def test_mock_request_empty_path() -> None:
    """Test that _mock_request handles an empty path correctly."""
    method = "GET"
    path = ""
    request = _mock_request(method, path)

    assert request.path == ""
    assert request.method == method

def test_mock_request_multiple_requests() -> None:
    """Test that multiple calls to _mock_request return distinct request objects."""
    method = "GET"
    paths = ["/path1", "/path2", "/path3"]
    requests = [_mock_request(method, path) for path in paths]

    for i, request in enumerate(requests):
        assert request.method == method
        assert request.path == paths[i]
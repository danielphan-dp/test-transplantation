import asyncio
from unittest import mock
import pytest
from aiohttp import web
from aiohttp.http import HttpVersion
from aiohttp.http import RawRequestMessage
from multidict import CIMultiDictProxy, CIMultiDict
from yarl import URL

def test_mock_request_creation() -> None:
    """Test the creation of a mock request with various methods and paths."""
    
    methods = ["GET", "POST", "PUT", "DELETE"]
    paths = ["/api/test", "/api/test/1", "/api/test/1/details", "/api/test/2"]
    
    for method in methods:
        for path in paths:
            request = _mock_request(method=method, path=path)
            assert request.method == method
            assert request.path == path
            assert request.version == HttpVersion(1, 1)
            assert request.host.lower() in socket.getfqdn().lower()
            assert request.keep_alive

def test_mock_request_with_headers() -> None:
    """Test the creation of a mock request with headers."""
    
    headers = CIMultiDict({"Content-Type": "application/json"})
    request = _mock_request(method="GET", path="/api/test", headers=headers)
    
    assert request.headers["Content-Type"] == "application/json"
    assert request.raw_headers == ((b"CONTENT-TYPE", b"application/json"),)

def test_mock_request_invalid_method() -> None:
    """Test the creation of a mock request with an invalid HTTP method."""
    
    with pytest.raises(ValueError):
        _mock_request(method="INVALID", path="/api/test")

def test_mock_request_empty_path() -> None:
    """Test the creation of a mock request with an empty path."""
    
    request = _mock_request(method="GET", path="")
    assert request.path == ""
    assert request.path_qs == ""

def test_mock_request_with_query_string() -> None:
    """Test the creation of a mock request with a query string."""
    
    request = _mock_request(method="GET", path="/api/test?param=value")
    assert request.query_string == "param=value"
    assert request.query.get("param") == "value"